from iconservice import *
from .IRC2 import TokenStandard

TAG = 'MySampleToken'

class TokenFallbackInterface(InterfaceScore):
    @interface
    def tokenFallback(self, _from: Address, _value: int, _data: bytes): pass


class MySampleToken(IconScoreBase,TokenStandard):
    _BALANCES = 'balances'
    _TOTAL_SUPPLY = 'total_supply'
    _DECIMALS = 'decimals'

    def __init__(self, db:IconScoreDatabase) -> None:
        super().__init__(db)

        self._total_supply = VarDB(self._TOTAL_SUPPLY, db, value_type=int)
        self._decimals = VarDB(self._DECIMALS, db, value_type=int)
        self._balances = DictDB(self._BALANCES, db, value_type= int)

    def on_install(self, initialSupply: int , decimals: int ) -> None:
        super().on_install()
        initialSupply = 800460000
        decimals = 18
        total_supply = initialSupply * 10 ** decimals

        self._total_supply.set(total_supply)
        self._decimals.set(decimals)
        self._balances[self.msg.sender] = total_supply

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def name(self) -> str:
        return "MySampleToken"

    @external(readonly=True)
    def symbol(self) -> str:
        return "MST"

    @external(readonly=True)
    def decimals(self) -> int:
        return self._decimals.get()
    
    @external(readonly=True)
    def totalSupply(self) -> int:
        return self._total_supply.get()

    @external(readonly=True)
    def balanceOf(self, _owner: Address) -> int:
        return self._balances[_owner]

    @eventlog(indexed=3)
    def Transfer(self, _from: Address, _to: Address, _value: int, _data: bytes): 
        pass


    @external
    def transfer(self, _to: Address, _value: Address, _data: bytes = None):
        if _data is None:
            _data = b'None'
        self._transfer(self.msg.sender, _to, _value, _data)

    def _transfer(self, _from: Address, _to: Address, _value: int, _data: bytes):
        if self._balances[_from] < _value:
            revert('Out of Balance')

        self._balances[_from] -= _value
        self._balances[_to] += _value 


        if _to.is_contract:
            recipient_score = self.create_interface_score(_to,TokenFallbackInterface)
            recipient_score.tokenFallback(_from, _value, _data)
        
        self.Transfer(_from,_to,_value,_data)
        
        Logger.debug(f'Transfer ({_from},{_to},{_value},{_data})',TAG)
