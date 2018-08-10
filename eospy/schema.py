import colander

class BaseSchema(colander.SchemaNode) :
    required = True

class StringSchema(BaseSchema) :
    schema_type = colander.String
    
# str schemas
class NameSchema(StringSchema) : pass 
class AccountNameSchema(NameSchema) : pass
class PermissionNameSchema(NameSchema) : pass
class ActionNameSchema(NameSchema) : pass
class TableNameSchema(NameSchema) : pass 
class ScopeNameSchema(NameSchema) : pass

# boolean
class BooleanSchema(BaseSchema) :
    schema_type = colander.Bool

# numeric

class IntSchema(BaseSchema) :
    schema_type = colander.Int

class HexBytesSchema(StringSchema) :
    missing = colander.drop

class DataSchema(StringSchema) : pass

# Authority/permission
class ThresholdSchema(IntSchema) : pass

class PublicKeySchema(StringSchema) : pass

class WeightSchema(IntSchema) : pass 

class KeyWeightSchema(colander.MappingSchema):
    key = PublicKeySchema()
    weight = WeightSchema()

class KeyWeightsSchema(colander.SequenceSchema) :
    key = KeyWeightSchema()

class PermissionLevelSchema(colander.MappingSchema) :
    actor = AccountNameSchema()
    permission = PermissionNameSchema()

class PermissionLevelsSchema(colander.SequenceSchema) :
    permission = PermissionLevelSchema()
    
class PermissionLevelWeightSchema(colander.MappingSchema) :
    permission = PermissionLevelSchema()
    weight = WeightSchema()
    
class PermissionLevelWeightsSchema(colander.SequenceSchema) :
    permission_level = PermissionLevelWeightSchema()

class WaitSecSchema(IntSchema) : pass
    
class WaitWeightSchema(colander.MappingSchema) :
    wait_sec = WaitSecSchema()
    weight = WeightSchema()
    
class WaitWeightsSchema(colander.SequenceSchema) :
    waits = WaitWeightSchema()
    
class AuthoritySchema(colander.MappingSchema) :
    threshold = ThresholdSchema()
    keys = KeyWeightsSchema()
    accounts = PermissionLevelWeightsSchema()
    waits = WaitWeightsSchema()

class PermNameSchema(BaseSchema) :
    schema_type = colander.String

class ParentSchema(StringSchema) : pass

class PermissionSchema(colander.MappingSchema) :
    perm_name = PermNameSchema()
    parent = ParentSchema()
    required_auth = AuthoritySchema()
    
#############################
# message actions attributes
#############################

class ActionSchema(colander.MappingSchema) :
    account = AccountNameSchema()
    name = ActionNameSchema()
    authorization = PermissionLevelsSchema()
    hex_data = HexBytesSchema()
    data = DataSchema()
    
class ActionsSchema(colander.SequenceSchema) :
    action = ActionSchema()

class ContextActionsSchema(colander.SequenceSchema) :
    action = ActionSchema()
    default = []
    missing = []

class ExtensionSchema(colander.MappingSchema) :
    type = IntSchema()
    data = HexBytesSchema()

class ExtensionsSchema(colander.SequenceSchema) :
    extension = ExtensionSchema()
    default = []
    missing = []
    
#############################
# message header attributes
#############################

class TimeSchema(BaseSchema) :
    schema_type = colander.DateTime

class RefBlockNumSchema(IntSchema) : pass
class RefBlockPrefixSchema(IntSchema) : pass
class NetUsageWordsSchema(IntSchema) :
    default = 0
    missing = 0
class MaxCpuUsageMsSchema(IntSchema) :
    default = 0
    missing = 0
class DelaySecSchema(IntSchema) :
    default = 0
    missing = 0

class SignaturesSchema(colander.Sequence) :
    signatures = StringSchema()
      
class TransactionSchema(colander.MappingSchema) :
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
class SignedTransactionSchema(colander.MappingSchema) :
    compression = StringSchema
    transaction = TransactionSchema()
    signatures = SignaturesSchema()

# final transaction
class PushTransactionSchema(colander.MappingSchema) :
    transaction_id = StringSchema()
    broadcast = BooleanSchema()
    transaction = SignedTransactionSchema()
    
class TransactionsSchema(colander.SequenceSchema) :
    transactions = TransactionSchema()
    
#############################
# get info
#############################

class ChainInfoSchema(colander.MappingSchema) :
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

class ProducerSchema(colander.SchemaNode) :
    schema_type = colander.String
    missing = 'null'
    default = 'null'
    required = False

class HeaderExtsSchema(colander.SequenceSchema) :
    header_extensions = ExtensionsSchema()

class BlockExtsSchema(colander.SequenceSchema) :
    block_extensions = ExtensionsSchema()

class BlockInfoSchema(colander.MappingSchema) :
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
