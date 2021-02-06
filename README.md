# stocksplit_dbkeeper

Stock Split Database Keeper do all complicated things so users can simply update and query the data.

## Methods Discover

**class |** DBKeeper ( db_folder_path: `str` )

* **func |** update ( symbol: `str`, data: `dict` )
* **func |** query_stocksplit ( symbol: `str` ) **->** query_data: `dict` / false_if_symbol_not_exists: `bool`
* **func |** query_master_info ( symbol: `str` ) **->** master_info: `dict` / false_if_symbol_not_exists: `bool`
* **func |** query_full_master_info ( ) **->** full_master_info: `dict`
