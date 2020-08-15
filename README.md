## 사용방법 

- `library/cf.py.bak`을 `cf.py`로 이름 변경 후 *db_ip, db_id, db_passwd, db_port, imi1_accout, imi1_simul_num, start_daily_buy_list, dart_api_key* 값을 본인의 설정에 맞게 변경 하시거나 
기존에 사용하던 `cf.py`를 library폴더 안에 복사 붙여 넣기 해주시기 바랍니다. 

- etf 사용 시
    `cf.py`에서 `use_etf = True` 로 설정  

- 추가 스크립트 
    - `fetch_etf.py` : etf 사용 시 daily_buy_list를 삭제하지 않고 기존에 만들어진 daily_buy_list 날짜 테이블에 etf 종목을 추가 해주는 스크립트  
        - **사용 시 유의사항** : `cf.py`의 `use_etf`를 `True`로 설정 하고 콜렉터를 돌려서 daily_craw db에 etf종목 테이블이 모두 생성 된 이후에 스크립트를 돌리시면 됩니다. 해당 스크립트는 장시간을 포함하여 언제든 돌리셔도 괜찮습니다.스크립트가 완벽히 다 돌아가서 daily_buy_list db의 날짜 테이블에 etf 종목을 모두 업데이트를 하게 되면 향후에는 콜렉터를 돌려도 daily_buy_list에 etf를 포함해서 날짜테이블이 생성 됩니다. 따라서 따로 `fetch_etf.py`를 사용하실 일이 없습니다.
            
    - `delete_rows_in.py` : 콜렉터를 실수로 장중에 돌리셔서 부정확한 데이터가 들어오게 될 경우 특정 날짜 이후로의 데이터를 daily_craw, daily_buy_list 에서 모두 지워주는 스크립트
        
