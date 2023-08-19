# 비트코인 계좌 조회를 위한 모듈 
from cryptos import *
# 비트코인 트랜잭션 조회를 위한 reuqests 모듈
import requests
# 비트코인 관계도 그림을 위한 Graphviz 모듈
import pydot

# 비트코인 모듈 선언
c = Bitcoin()
# 관계도 그림을 위한 graphviz 설정
# rankdir = "LR" 위에서 아래로 가 아닌 좌에서 우로 그림이 그려져서
# 노드가 많을수록 보기가 편해짐
graph = pydot.Dot('my_graph', graph_type='digraph', rankdir='LR')



# 해당 비트코인 가상 계좌의 잔액을 확인하기 위한 함수
def getBalance(addr):
    count = 0
    while True:
        print(addr)
        try:
            total = 0
            inputs = c.unspent(addr)
        
                    
            # 잔액 계산을 더하기 위한 total 변수 0 으로 설정
            
            # 비트코인 addr 계좌의 트랜잭션들을 전부 탐색
            for i in inputs:
                # total 변수에 태랜잭션의 결과값을 전부 더하면 해당 계좌의 잔액이 확이됨
                total += i["value"]
            # addr 계좌의 잔액이 리턴
            break
        except:
            pass
    return total


def relationship(addr):
	
	# 조사할 비트코인 계좌의 노드 생성
	# label 에 실제 그림에 입력될 노드 이름이 설정된다
	graph.add_node(pydot.Node(addr, label = addr + "_" + str(getBalance(addr))))
	while True:
		try:
			# 비트코인 addr 계좌의 전체 트랜잭션들을 호출			
			inputs = c.unspent(addr)
			break
		except:
			continue
	tmp = []
	# 비트코인 addr 계좌의 전체 트랜잭션을 탐색
	for i in inputs:
		# tx_hash에 트랜잭션의 고유 주소값을 부여
		tx_hash = i["tx_hash"]
		# blockchain.info 에 api 형태로 해당 트랜잭션 주소의 결과값을 요청
		response = requests.get("https://api.blockchain.info/haskoin-store/btc/transaction/" + tx_hash )
		# 요청된 결과값 중 잔액을 조회하여 0원 인 계좌는 그림의 대상이 아님
		for output in response.json()["outputs"]:
			# tmp 리스트에 edge 로 설정될 주소가 있다면 패스
			if "address" in output and output["address"] != addr and output["address"] not in tmp:
				address = output["address"]
				# 트랜잭션의 대상이 되는 계좌가 비트코인 계좌일 경우 판단
				if address.startswith("1") or address.startswith("3"):
					# 해당 트랜잭션의 대상이 되는 비트코인 계좌의 잔액을 호출
					balance = getBalance(address)
					# 해당 잔액이 0원이 아닐경우
					if balance > 0:						
						print(tx_hash, address, balance)	
						# graphviz 를 통해 해당 계좌의 노드를 생성    				
						graph.add_node(pydot.Node(address, label = address + "_" + str(balance)))
						# 생성된 계좌의 노드를 Edge 로 관계를 표현
						graph.add_edge(pydot.Edge(addr, address))
						# 후에 중복된 edge 로 표현되지 않게 tmp 리스트에 해당 계좌를 담는다
						tmp.append(address)	
	return tmp
	

# 조사할 비트코인 계좌

addr = "1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd"
tmps = relationship(addr)
for addr in tmps:
    relationship(addr)
# bitcoin.png 로 저장
graph.write_png("bitcoin.png")
