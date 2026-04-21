import re
import unicodedata
from dataclasses import dataclass

CURRENT_YEAR = 2026

@dataclass
class Spec:
    year: int
    measure: str
    dimensions: list[str]

class GroupedAggregateGenerator:
    def normalize(self, q: str) -> str:
        q = q.strip().rstrip('?').lower()
        q = unicodedata.normalize('NFKD', q).encode('ascii','ignore').decode('ascii')
        return q

    def parse(self, question: str) -> Spec:
        q = self.normalize(question)
        year = 2026 if ('2026' in q or 'ano atual' in q or 'este ano' in q or 'ano corrente' in q) else None
        if not year:
            raise ValueError('Ano não identificado')

        if 'diferenca entre o preco de lista zlp1 e o valor liquido faturado' in q or 'diferenca entre preco de lista e valor liquido faturado' in q or 'diferenca entre o preco de lista e o valor liquido faturado' in q:
            measure = 'list_minus_net'
        elif 'descontos de quantidade' in q:
            measure = 'qty_discount'
        elif 'quantidade faturada e a quantidade em unidade base' in q:
            measure = 'qty_and_base'
        elif 'peso bruto total' in q:
            measure = 'gross_weight_total'
        elif 'diferenca entre quantidade faturada e quantidade em unidade base' in q:
            measure = 'qty_minus_base'
        elif 'peso liquido total' in q:
            measure = 'net_weight_total'
        elif 'valor liquido faturado' in q or 'faturacao' in q:
            measure = 'net_amount'
        else:
            raise ValueError('Métrica fora do escopo grouped_aggregate revP')

        dims = []
        checks = [
            ('pais da regiao do cliente', 'customer_region_country'),
            ('grupo de contas do cliente', 'customer_account_group'),
            ('condicao de expedicao do cliente', 'shipping_condition'),
            ('zona de transporte do cliente', 'transp_zone'),
            ('tipo de lista de precos', 'price_list_type'),
            ('price list type', 'price_list_type'),
            ('tipo de documento de faturacao', 'billing_doc_type'),
            ('tipo de documento', 'billing_doc_type'),
            ('categoria de documento de faturacao', 'billing_doc_category'),
            ('categoria de documento', 'billing_doc_category'),
            ('pais de partida', 'departure_country'),
            ('pais de expedicao', 'departure_country'),
            ('organizacao de vendas', 'sales_org'),
            ('canal de distribuicao', 'dist_channel'),
            (' e canal', 'dist_channel'),
            (' por canal', 'dist_channel'),
            ('grupo de cliente', 'customer_group'),
            ('por produto', 'product'),
            ('unidade de peso', 'weight_unit'),
            ('marca de produto', 'product_brand'),
            (' por marca', 'product_brand'),
            (' por brand', 'product_brand'),
            ('familia de produto', 'product_family'),
            ('product family', 'product_family'),
            ('tipo de material', 'material_type'),
            ('material type', 'material_type'),
            (' por pais', 'country'),
        ]
        for needle, key in checks:
            if needle in q and key not in dims:
                dims.append(key)
        if 'grupo de contas do cliente' in q and 'customer_group' in dims:
            dims.remove('customer_group')
        if 'pais da regiao do cliente' in q and 'country' in dims:
            dims.remove('country')
        if ('pais de partida' in q or 'pais de expedicao' in q) and 'country' in dims:
            dims.remove('country')
        if not dims:
            raise ValueError('Dimensão não identificada')
        return Spec(year=year, measure=measure, dimensions=dims)

    def _measure_sql(self, measure: str):
        if measure == 'net_amount':
            return 'SUM(f.NetAmount) AS ValorLiquidoFaturado', 'ValorLiquidoFaturado', 'DESC'
        if measure == 'list_minus_net':
            return 'SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido', 'DiferencaPrecoListaVsLiquido', 'DESC'
        if measure == 'qty_discount':
            return 'SUM(f.ZDQ1QtyDiscount) AS DescontoQuantidade', 'DescontoQuantidade', 'ASC'
        if measure == 'qty_and_base':
            return 'SUM(f.BillingQuantity) AS QuantidadeFaturada,\n    SUM(f.BillingQuantityInBaseUnit) AS QuantidadeEmUnidadeBase', None, None
        if measure == 'gross_weight_total':
            return 'SUM(f.ItemGrossWeight) AS PesoBrutoTotal', 'PesoBrutoTotal', 'DESC'
        if measure == 'qty_minus_base':
            return 'SUM(f.BillingQuantity) - SUM(f.BillingQuantityInBaseUnit) AS DiferencaQuantidadeFaturadaVsBase', 'DiferencaQuantidadeFaturadaVsBase', 'DESC'
        if measure == 'net_weight_total':
            return 'SUM(f.ItemNetWeight) AS PesoLiquidoTotal', 'PesoLiquidoTotal', 'DESC'
        raise ValueError(measure)

    def _dim_sql(self, dims: list[str]):
        joins=[]; selects=[]; groups=[]
        for d in dims:
            if d == 'sales_org':
                joins.append('JOIN dbo.D_SalesOrganization so\n    ON f.NIDSalesOrganization = so.NIDSalesOrganization')
                selects.append('so.TSalesOrganization AS OrganizacaoVendas'); groups.append('so.TSalesOrganization')
            elif d == 'dist_channel':
                joins.append('JOIN dbo.D_DistributionChannel dc\n    ON f.NIDDistributionChannel = dc.NIDDistributionChannel')
                selects.append('dc.TDistributionChannel AS CanalDistribuicao'); groups.append('dc.TDistributionChannel')
            elif d == 'price_list_type':
                joins.append('JOIN dbo.D_PriceListType plt\n    ON f.NIDPriceListType = plt.NIDPriceListType')
                selects.append('plt.TPriceListType AS TipoListaPrecos'); groups.append('plt.TPriceListType')
            elif d == 'customer_group':
                joins.append('JOIN dbo.D_CustomerGroup cg\n    ON f.NIDCustomerGroup = cg.NIDCustomerGroup')
                selects.append('cg.TCustomerGroup AS GrupoCliente'); groups.append('cg.TCustomerGroup')
            elif d == 'customer_account_group':
                joins.append('JOIN dbo.D_Customer c\n    ON f.NIDPayerParty = c.NIDCustomer')
                joins.append('JOIN dbo.D_CustomerAccountGroup cag\n    ON c.NIDCustomerAccountGroup = cag.NIDCustomerAccountGroup')
                selects.append('cag.TCustomerAccountGroup AS GrupoContasCliente'); groups.append('cag.TCustomerAccountGroup')
            elif d == 'shipping_condition':
                joins.append('JOIN dbo.D_Customer c\n    ON f.NIDPayerParty = c.NIDCustomer')
                joins.append('JOIN dbo.D_ShippingCondition sc\n    ON c.NIDShippingCondition = sc.NIDShippingCondition')
                selects.append('sc.TShippingCondition AS CondicaoExpedicao'); groups.append('sc.TShippingCondition')
            elif d == 'transp_zone':
                joins.append('JOIN dbo.D_Customer c\n    ON f.NIDPayerParty = c.NIDCustomer')
                joins.append('JOIN dbo.D_TranspZone tz\n    ON c.NIDTranspZone = tz.NIDTranspZone')
                selects.append('tz.TTranspZone AS ZonaTransporte'); groups.append('tz.TTranspZone')
            elif d == 'customer_region_country':
                joins.append('JOIN dbo.D_Customer c\n    ON f.NIDPayerParty = c.NIDCustomer')
                joins.append('JOIN dbo.D_Country co\n    ON c.NIDCountryRegion = co.NIDCountry')
                selects.append('co.TCountry AS PaisRegiaoCliente'); groups.append('co.TCountry')
            elif d == 'product':
                joins.append('JOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct')
                selects.append('p.TProduct AS Produto'); groups.append('p.TProduct')
            elif d == 'weight_unit':
                joins.append('JOIN dbo.D_UnitOfMeasure u\n    ON f.NIDItemWeightUnitSAPCode = u.NIDUnitOfMeasure')
                selects.append('u.TUnitOfMeasure AS UnidadePeso'); groups.append('u.TUnitOfMeasure')
            elif d == 'product_brand':
                joins.append('JOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct')
                joins.append('JOIN dbo.D_ProductBrand pb\n    ON p.NIDProductBrand = pb.NIDProductBrand')
                selects.append('pb.TProductBrand AS MarcaProduto'); groups.append('pb.TProductBrand')
            elif d == 'product_family':
                joins.append('JOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct')
                joins.append('JOIN dbo.D_ProductFamily pf\n    ON p.NIDProductFamily = pf.NIDProductFamily')
                selects.append('pf.TProductFamily AS FamiliaProduto'); groups.append('pf.TProductFamily')
            elif d == 'material_type':
                joins.append('JOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct')
                joins.append('JOIN dbo.D_MaterialType mt\n    ON p.NIDMaterialType = mt.NIDMaterialType')
                selects.append('mt.TMaterialType AS TipoMaterial'); groups.append('mt.TMaterialType')
            elif d == 'country':
                joins.append('JOIN dbo.D_Country co\n    ON f.NIDCountry = co.NIDCountry')
                selects.append('co.TCountry AS Pais'); groups.append('co.TCountry')
            elif d == 'departure_country':
                joins.append('JOIN dbo.D_Country co\n    ON f.NIDDepartureCountry = co.NIDCountry')
                selects.append('co.TCountry AS PaisPartida'); groups.append('co.TCountry')
            elif d == 'billing_doc_type':
                joins.append('JOIN dbo.D_BillingDocumentType bdt\n    ON f.NIDBillingDocumentType = bdt.NIDBillingDocumentType')
                selects.append('bdt.TBillingDocumentType AS TipoDocumentoFaturacao'); groups.append('bdt.TBillingDocumentType')
            elif d == 'billing_doc_category':
                joins.append('JOIN dbo.D_BillingDocumentCategory bdc\n    ON f.NIDBillingDocumentCategory = bdc.NIDBillingDocumentCategory')
                selects.append('bdc.TBillingDocumentCategory AS CategoriaDocumentoFaturacao'); groups.append('bdc.TBillingDocumentCategory')
            else:
                raise ValueError(d)
        unique_joins=[]
        for j in joins:
            if j not in unique_joins:
                unique_joins.append(j)
        return unique_joins, selects, groups

    def generate(self, question: str) -> str:
        spec=self.parse(question)
        measure_sql, order_alias, order_dir = self._measure_sql(spec.measure)
        joins, selects, groups = self._dim_sql(spec.dimensions)
        select_clause = ',\n    '.join(selects + [measure_sql])
        sql = 'SELECT\n    ' + select_clause + '\nFROM dbo.F_Invoice f\n'
        if joins:
            sql += '\n'.join(joins) + '\n'
        sql += f'WHERE f.BillingDocumentDate / 10000 = {spec.year}\n  AND f.BillingDocumentIsCancelled = 0\n'
        sql += 'GROUP BY ' + ', '.join(groups) + '\n'
        if spec.measure == 'qty_and_base':
            sql += f'ORDER BY {groups[0]};'
        else:
            sql += f'ORDER BY {order_alias} {order_dir};'
        return sql
