import colander

class BaseSchema(colander.SchemaNode):
    required = True

class StringSchema(BaseSchema):
    schema_type = colander.String
    
# str schemas
class NameSchema(StringSchema): pass 
class AccountNameSchema(NameSchema): pass
class PermissionNameSchema(NameSchema): pass
class ActionNameSchema(NameSchema): pass
class TableNameSchema(NameSchema): pass 
class ScopeNameSchema(NameSchema): pass

# boolean
class BooleanSchema(BaseSchema):
    schema_type = colander.Bool

# numeric

class IntSchema(BaseSchema):
    schema_type = colander.Int

class HexBytesSchema(StringSchema):
    missing = colander.drop

# Authority/permission
class ThresholdSchema(IntSchema): pass

class PublicKeySchema(StringSchema): pass

class WeightSchema(IntSchema): pass 

class KeyWeightSchema(colander.MappingSchema):
    key = PublicKeySchema()
    weight = WeightSchema()

class KeyWeightsSchema(colander.SequenceSchema):
    key = KeyWeightSchema()

class PermissionLevelSchema(colander.MappingSchema):
    actor = AccountNameSchema()
    permission = PermissionNameSchema()

class PermissionLevelsSchema(colander.SequenceSchema):
    permission = PermissionLevelSchema()
    
class PermissionLevelWeightSchema(colander.MappingSchema):
    permission = PermissionLevelSchema()
    weight = WeightSchema()
    
class PermissionLevelWeightsSchema(colander.SequenceSchema):
    permission_level = PermissionLevelWeightSchema()

class WaitSecSchema(IntSchema): pass
    
class WaitWeightSchema(colander.MappingSchema):
    wait_sec = WaitSecSchema()
    weight = WeightSchema()
    
class WaitWeightsSchema(colander.SequenceSchema):
    waits = WaitWeightSchema()
    
class AuthoritySchema(colander.MappingSchema):
    threshold = ThresholdSchema()
    keys = KeyWeightsSchema()
    accounts = PermissionLevelWeightsSchema()
    waits = WaitWeightsSchema()

class PermNameSchema(BaseSchema):
    schema_type = colander.String

class ParentSchema(StringSchema): pass

class PermissionSchema(colander.MappingSchema):
    perm_name = PermNameSchema()
    parent = ParentSchema()
    required_auth = AuthoritySchema()
    
# def validate_data_schema(node, value):
#     if not isinstance(value, dict) or not isinstance(value, str):
#         raise colander.Invalid(node, '{} is not a valid data schema'.format(value))

class DataSchema(colander.SchemaType): 
    
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        impl = colander.Mapping()
        if isinstance(appstruct, str):
            impl = StringSchema()
        return impl.serialize(node, appstruct)

    def deserialize(self, node, cstruct):
        return cstruct

#############################
# message actions attributes
#############################

class ActionSchema(colander.MappingSchema):
    account = AccountNameSchema()
    name = ActionNameSchema()
    authorization = PermissionLevelsSchema()
    # if data is there it can be a HexBytesSchema or DataSchema
    hex_data = HexBytesSchema()
    data = colander.SchemaNode(DataSchema())

class ActionsSchema(colander.SequenceSchema):
    action = ActionSchema()

class ContextActionsSchema(colander.SequenceSchema):
    default = []
    missing = []
    action = ActionSchema()

class ExtensionSchema(colander.MappingSchema):
    type = IntSchema()
    data = HexBytesSchema()

class ExtensionsSchema(colander.SequenceSchema):
    default = []
    missing = []
    extension = ExtensionSchema()
    
#############################
# message header attributes
#############################

class TimeSchema(BaseSchema):
    schema_type = colander.DateTime

class RefBlockNumSchema(IntSchema): pass
class RefBlockPrefixSchema(IntSchema): pass
class NetUsageWordsSchema(IntSchema):
    default = 0
    missing = 0
class MaxCpuUsageMsSchema(IntSchema):
    default = 0
    missing = 0
class DelaySecSchema(IntSchema):
    default = 0
    missing = 0

class SignaturesSchema(colander.Sequence):
    signatures = StringSchema()
      
class TransactionSchema(colander.MappingSchema):
    # header
    expiration = TimeSchema()
    ref_block_num = RefBlockNumSchema()
    ref_block_prefix = RefBlockPrefixSchema()
    net_usage_words = NetUsageWordsSchema()
    max_cpu_usage_ms = MaxCpuUsageMsSchema()
    delay_sec = DelaySecSchema()
    # body
    context_free_actions = ContextActionsSchema()
    actions = ActionsSchema()
    transaction_extensions = ExtensionsSchema()

# signed transaction
class SignedTransactionSchema(colander.MappingSchema):
    compression = StringSchema
    transaction = TransactionSchema()
    signatures = SignaturesSchema()

# final transaction
class PushTransactionSchema(colander.MappingSchema):
    transaction_id = StringSchema()
    broadcast = BooleanSchema()
    transaction = SignedTransactionSchema()
    
class TransactionsSchema(colander.SequenceSchema):
    transactions = TransactionSchema()
    
#############################
# get info
#############################

class ChainInfoSchema(colander.MappingSchema):
    server_version = StringSchema()
    chain_id = StringSchema()
    head_block_num = IntSchema()
    last_irreversible_block_num = IntSchema()
    last_irreversible_block_id = StringSchema()
    head_block_id  = StringSchema()
    head_block_time = TimeSchema()
    head_block_producer = StringSchema()
    virtual_block_cpu_limit = IntSchema()
    virtual_block_net_limit = IntSchema()
    block_cpu_limit = IntSchema()
    block_net_limit = IntSchema()

#############################
# get block
#############################

class ProducerSchema(colander.SchemaNode):
    schema_type = colander.String
    missing = 'null'
    default = 'null'
    required = False

class HeaderExtsSchema(colander.SequenceSchema):
    header_extensions = ExtensionsSchema()

class BlockExtsSchema(colander.SequenceSchema):
    block_extensions = ExtensionsSchema()

class BlockInfoSchema(colander.MappingSchema):
    timestamp = TimeSchema()
    producer = StringSchema()
    confirmed = IntSchema()
    previous = StringSchema()
    transaction_mroot = StringSchema()
    action_mroot = StringSchema()
    schedule_version = IntSchema
    new_producers = ProducerSchema()
    header_extensions = HeaderExtsSchema()
    producer_signature = StringSchema
    # TODO
    #transactions = [],
    block_extensions = BlockExtsSchema()
    id = StringSchema()
    block_num = IntSchema()
    ref_block_prefix = IntSchema()

#############################
# abi
#############################

class AbiTypeSchema(colander.MappingSchema):
    new_type_name = StringSchema()
    type = StringSchema()

class AbiTypesSchema(colander.SequenceSchema):
    default = []
    missing = []
    types = AbiTypeSchema()

class AbiStructFieldSchema(colander.MappingSchema):
    name = StringSchema()
    type = StringSchema()

class AbiStructFieldsSchema(colander.SequenceSchema):
    default = []
    missing = []
    fields = AbiStructFieldSchema()

class AbiStructBaseSchema(StringSchema):
    default = ""
    missing = ""

class AbiStructSchema(colander.MappingSchema):
    name = StringSchema()
    base = AbiStructBaseSchema()
    fields = AbiStructFieldsSchema()

class AbiStructsSchema(colander.SequenceSchema):
    structs = AbiStructSchema()

class AbiRicardianStrSchema(StringSchema):
    required = False

class AbiActionSchema(colander.MappingSchema):
    name = StringSchema()
    type = StringSchema()
    ricardian_contract = AbiRicardianStrSchema

class AbiActionsSchema(colander.SequenceSchema):
    actions = AbiActionSchema()

class AbiTableKey(StringSchema): pass
    # required = False

class AbiTablesKey(colander.SequenceSchema):
    default = []
    missing = []
    keys = AbiTableKey()

class AbiTableSchema(colander.MappingSchema):
    name = StringSchema()
    index_type = StringSchema()
    key_names = AbiTablesKey()
    key_types = AbiTablesKey()
    type = StringSchema()

class AbiTablesSchema(colander.SequenceSchema):
    missing = []
    default = []
    tables = AbiTableSchema()

class AbiRicardianClauseSchema(colander.MappingSchema):
    id = StringSchema()
    body = StringSchema()

class AbiRicardianClausesSchema(colander.SequenceSchema):
    required = False
    missing = []
    default = []
    rcs = AbiRicardianClauseSchema()

# placeholder
class AbiErrorMessageSchema(StringSchema): 
    required = False

class AbiErrorMessagesSchema(colander.SequenceSchema):
    default = []
    missing = []
    required = False
    error_messages = AbiErrorMessageSchema()

# placeholder
class AbiExtensionSchema(StringSchema): 
    required = False

class AbiExtensionsSchema(colander.SequenceSchema):
    default = []
    missing = []
    required = False
    abi_extensions = AbiExtensionSchema()

# placeholder
class AbiVariantSchema(StringSchema): 
    required = False

class AbiVariantsSchema(colander.SequenceSchema):
    default = []
    missing = []
    required = False
    variants = AbiVariantSchema()

class AbiCommentSchema(StringSchema): 
    required = False
    default = ""
    missing = ""

class AbiSchema(colander.MappingSchema):
    version = StringSchema()
    types = AbiTypesSchema()
    structs = AbiStructsSchema()
    actions = AbiActionsSchema()
    tables = AbiTablesSchema()
    ricardian_clauses = AbiRicardianClausesSchema()
    error_messages = AbiErrorMessagesSchema()
    abi_extensions = AbiExtensionsSchema()
    variants = AbiVariantsSchema()

#############################
# eosytest
#############################

def test_param_validator(node, value):
    if not isinstance(value, dict):
        raise colander.Invalid(node, '{} is not a valid dictionary'.format(value))

class TestEnvSchema(colander.MappingSchema):
    url = StringSchema()

class TestAuthSchema(colander.MappingSchema):
    actor = StringSchema()
    permission = StringSchema()
    key = StringSchema()

class TestActionSchema(colander.MappingSchema):
    action = StringSchema()
    contract = StringSchema()
    authorization = TestAuthSchema()
    parameters = colander.SchemaNode(
        colander.Mapping(unknown='preserve'),
        validator=test_param_validator
    )
    exception = BooleanSchema()

class TestActionsSchema(colander.SequenceSchema):
    actions = TestActionSchema()

class TestSchema(colander.MappingSchema):
    name = StringSchema()
    actions = TestActionsSchema()

class TestsSchema(colander.SequenceSchema):
    tests = TestSchema()

class TestDocSchema(colander.MappingSchema):
    environment = TestEnvSchema()
    tests = TestsSchema()