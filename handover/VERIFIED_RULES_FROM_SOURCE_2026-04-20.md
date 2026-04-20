# Regras verificadas a partir da documentação-fonte — 2026-04-20

## Âncora e joins
- `dbo.F_Invoice` é a âncora central.
- Cliente: `f.NIDPayerParty = c.NIDCustomer`.
- Produto: `f.NIDProduct = p.NIDProduct`.
- Não ligar `F_Invoice` diretamente a `D_ProductBrand`, `D_ProductFamily` ou `D_MaterialType`; usar via `D_Product`.
- Não ligar `F_Invoice` diretamente a `D_ShippingCondition`, `D_TranspZone` ou `D_CustomerAccountGroup`; usar via `D_Customer`.
- Para apresentação, preferir rótulos de negócio `T...` em vez de chaves técnicas `NID...`.

## Defaults de negócio
- Para perguntas de faturação e vendas, excluir cancelados por defeito com `BillingDocumentIsCancelled = 0`, salvo perguntas sobre cancelamentos.
- Valor líquido faturado: `SUM(f.NetAmount)`.
- Quantidade faturada: `SUM(f.BillingQuantity)`.
- Preço de lista: `SUM(f.ZLP1PriceList)`.
- Desconto de quantidade: `SUM(f.ZDQ1QtyDiscount)`.
- Desconto promocional total: `SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)`.
- Preço médio líquido por unidade: `SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0)`.
- Peso líquido médio por unidade: `SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0)`.
- Peso bruto total por unidade de peso: somar `ItemGrossWeight` por unidade; não dividir por quantidade.
- Quantidade em unidade base: `SUM(f.BillingQuantityInBaseUnit)`.

## Guardrails críticos
- Para `GrossMargin` e `NetCommercialSales`, o comportamento mais estável é com `IsItAnAdditionalCalculatedRecord = 1` quando relevante.
- Em percentagens e quotas, devolver escala 0-100.
- Usar sempre `NULLIF` no denominador.
- Para preço médio/peso médio por unidade, não filtrar `BillingQuantity <> 0` ao nível da linha quando o contrato exige exclusão ao nível agregado.
- Para valor líquido absoluto por documento, usar `ABS(SUM(f.NetAmount))` ao nível do documento; não `SUM(ABS(f.NetAmount))`.
- Para taxa de cancelamento, consolidar primeiro ao nível de `BillingDocument` e só depois agregar por mês/dimensão.
- Para comparações 2025 vs 2026 no mesmo eixo, preferir um único agregado com `CASE WHEN` em vez de dois joins separados à facto.
- Em top N dentro de grupo, usar `ROW_NUMBER() OVER (PARTITION BY ...)` e filtrar fora `rn <= N`.
- Em SQL Server, não usar `QUALIFY`, `LIMIT` ou `FETCH FIRST`.

## Semânticas proibidas
- Não substituir grupo de contas de cliente por grupo de cliente.
- Não substituir condição de expedição por shipping point.
- Não substituir zona de transporte por sales district.
- Não substituir país de origem do cliente por `F_Invoice.NIDCountry`.
- Não substituir região do cliente pela região direta da linha de faturação quando a pergunta menciona explicitamente cliente.
- Quando a pergunta usa códigos de negócio como organização `1000` ou canal `10`, filtrar pelos campos de código da dimensão, não pelos IDs surrogate da facto.

## Pontos ainda em aberto
- Semântica exata de `CancelledBillingDocument`.
- Semântica exata de `ReferenceSDDocumentItem`.
- Papel exato de `F_Invoice.NIDCountry` sem mais contexto documental.
