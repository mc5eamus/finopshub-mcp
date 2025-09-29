    Costs returns the following fields:
    AvailabilityZone: Area within a resource location for high availability (not available for all services)
    BilledCost: Amount owed after discounts — basis for invoicing
    BillingAccountId: Unique ID for the billing account or profile
    BillingAccountName: Display name of the billing account or profile
    BillingAccountType: Type of billing account (EA, MCA, MG, MOSA, etc.)
    BillingCurrency: Currency code for all billing cost columns
    BillingPeriodEnd: Exclusive end datetime of the billing period
    BillingPeriodStart: Inclusive start datetime of the billing period
    ChargeCategory: High-level classification of a charge (Usage, Purchase, Credit, Adjustment, Tax)
    ChargeClass: Indicates if row is a correction (e.g., Correction)
    ChargeDescription: Human-readable summary of the charge
    ChargeFrequency: How often the charge occurs (One-Time, Recurring, Usage-Based)
    ChargePeriodEnd: Exclusive end datetime of the charge period
    ChargePeriodStart: Inclusive start datetime of the charge period
    CommitmentDiscountCategory: Commitment discount by usage or spend
    CommitmentDiscountId: Unique ID (GUID) of applied commitment discount
    CommitmentDiscountName: Name of the commitment discount
    CommitmentDiscountStatus: Status (Consumed vs. Unused) of the commitment discount
    CommitmentDiscountType: Type of commitment (Reservation, Savings Plan)
    ConsumedQuantity: Volume of resource usage
    ConsumedUnit: Unit of measurement for consumed quantity
    ContractedCost: Cost = ContractedUnitPrice × PricingQuantity
    ContractedUnitPrice: Unit price after negotiated discounts (excluding commitment)
    EffectiveCost: Amortized cost after discounts and commitment
    InvoiceIssuerName: Entity name that issued the invoice
    ListCost: Retail cost before any discounts
    ListUnitPrice: Retail unit price before any discounts
    PricingCategory: Pricing model used (Standard, Dynamic, Committed)
    PricingQuantity: Measured usage quantity in pricing units
    PricingUnit: Unit of measurement for PricingQuantity
    PricingUnitDescription: Human-readable description of the pricing unit
    ProviderName: Name of provider offering the resources
    PublisherName: Name of organization that produced the resources
    RegionId: Provider-assigned geographic region ID
    RegionName: Name of the region where resource/service is provisioned
    ResourceId: Unique identifier of the resource
    ResourceName: Human-readable name of the resource
    ResourceType: Type/category of resource
    ServiceCategory: Top-level category of service
    ServiceName: Name of service offering
    SkuId: Unique identifier of SKU
    SkuPriceId: Unique identifier for unit price variation
    SubAccountId: ID for resource grouping (e.g., subscription)
    SubAccountName: Name of the resource grouping
    SubAccountType: Type label for resource grouping
    Tags: JSON object of custom tags (key/value)
    x_AccountId: ID of billing responsible identity (EA/MOSA)
    x_AccountName: Name of billing responsible identity
    x_AccountOwnerId: Email of billing responsible identity
    x_BilledCostInUsd: BilledCost converted to USD
    x_BilledUnitPrice: Unit price charged per PricingUnit
    x_BillingAccountAgreement: Billing agreement type (EA, MCA, etc.)
    x_BillingAccountId: BillingAccountId (Cost Management mapping)
    x_BillingAccountName: BillingAccountName (Cost Management mapping)
    x_BillingExchangeRate: Rate converting pricing to billing currency
    x_BillingExchangeRateDate: Date exchange rate was determined
    x_BillingProfileId: ID for MCA billing profile
    x_BillingProfileName: Name for MCA billing profile
    x_ChargeId: Unique identifier (GUID) for the charge
    x_ContractedCostInUsd: ContractedCost converted to USD
    x_CostAllocationRuleName: Cost Management allocation rule name
    x_CostCategories: Custom cost-category tags
    x_CostCenter: Internal cost center code
    x_Credits: Applied credits amount
    x_CostType: Type of cost (usage vs purchase)
    x_CurrencyConversionRate: Rate used for currency conversion
    x_CustomerId: CSP customer tenant ID
    x_CustomerName: CSP customer tenant name
    x_Discount: Amount discounted from list
    x_EffectiveCostInUsd: EffectiveCost converted to USD
    x_EffectiveUnitPrice: Amortized unit price after discounts
    x_ExportTime: Timestamp when data was exported
    x_IngestionTime: Timestamp when data was ingested
    x_InvoiceId: ID of the invoice
    x_InvoiceIssuerId: ID of entity that issued invoice
    x_InvoiceSectionId: GUID of invoice section or EA department
    x_InvoiceSectionName: Name of invoice section or department
    x_ListCostInUsd: ListCost converted to USD
    x_Location: Geographic location (alias for region)
    x_Operation: Operation name associated with usage
    x_PartnerCreditApplied: Flag if CSP partner credit applied
    x_PartnerCreditRate: Rate of CSP partner credit
    x_PricingBlockSize: Quantity block size for pricing rules
    x_PricingCurrency: Currency code used for pricing columns
    x_PricingSubcategory: Subcategory within pricing model
    x_PricingUnitDescription: Full description of PricingUnit including block
    x_Project: Project tag (custom)
    x_PublisherCategory: Indicates provider vs Marketplace vendor
    x_PublisherId: ID of publisher organization
    x_ResellerId: ID of CSP reseller
    x_ResellerName: Name of CSP reseller
    x_ResourceGroupName: Name of resource group
    x_ResourceType: Azure Resource Manager type code
    x_ServiceCode: Internal code for service
    x_ServiceId: Unique ID of service offering
    x_ServicePeriodEnd: Exclusive end datetime of service usage period
    x_ServicePeriodStart: Inclusive start datetime of service usage period
    x_SkuDescription: Description of the SKU
    x_SkuDetails: JSON with supplemental SKU info
    x_SkuIsCreditEligible: True if SKU eligible for Azure credits
    x_SkuMeterCategory: Category of the usage meter
    x_SkuMeterId: Unique identifier for the usage meter
    x_SkuMeterName: Name of the usage meter
    x_SkuMeterSubcategory: Subcategory of the meter
    x_SkuOfferId: Cloud subscription offer ID
    x_SkuOrderId: Entitlement product ID
    x_SkuOrderName: Entitlement product name
    x_SkuPartNumber: Part number identifier of the SKU
    x_SkuRegion: Region where SKU was active
    x_SkuServiceFamily: Functional family of the SKU
    x_SkuTerm: Commitment term in months
    x_SkuTier: Pricing tier of the SKU
    x_SourceChanges: Codes indicating data modifications
    x_SourceName: Source system or dataset name
    x_SourceProvider: Provider of source data
    x_SourceType: Type of export data (ActualCost, AmortizedCost, etc.)
    x_SourceVersion: Source schema version
    x_UsageType: Type of usage associated with the charge