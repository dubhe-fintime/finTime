import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 은행연합회 대출 상품 조회
# 방식 : API
# 수집 데이터
##############################

##############################
# Service URL = "https://portal.kfb.or.kr/compare/loan_search_search_result.php"
# Method = POST
##############################

async def getLoanData(InterestType):
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    product_list = []
    # API URL
    url =  "https://portal.kfb.or.kr/compare/loan_search_search_result.php"
    ######### 기초 설정 END ##############

    if InterestType == "Interest1":
        residence_type = "APT"
    elif InterestType == "Interest2":
        residence_type = "OTHER"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        body = {
            "InterestType": InterestType,
            "BankValue": "0010030|0013175|0011625|0010001|0010002|0013909|0010026|0010927|0014807|0010016|0010017|0010019|0010020|0010022|0010024|0014674|0015130|0017801",
            "INTEREST_TYPE": "All",
            "REPAY_TYPE": "All",
            "LoanMoney": "100000000",
            "LoanYear": "10",
            "SortType": ""
        }

        # 웹페이지 요청
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find("div", class_="data-container")

        # thead 제거
        if container and container.find("thead"):
            container.find("thead").decompose()

        products = container.find_all("tr")
        products = [product for product in products if product.get('id') != 'Goods_Text_TR']

        # 검색결과가 없을 때
        no_results = False

        # 검색결과가 없다는 텍스트가 있는 tr 태그가 있는지 확인
        for product in products:
            if "검색결과가 없습니다." in product.text:
                no_results = True
                break

        if no_results:
            print(f"대출 {residence_type} 상품 완료 | 결과 없음")
            return product_list
        
        for product in products:
            # 각 상품의 정보 추출
            columns = product.find_all("td")
            if len(columns) < 6:
                continue  # 필수 정보가 없으면 건너뛰기

            # 각 항목 추출
            bank_name = columns[0].text.strip()
            product_name = columns[1].text.replace("\n", "").strip()
            interest_method = columns[2].text.strip()
            repayment_method = columns[3].text.strip()
            min_interest = columns[4].text.strip()
            max_interest = columns[5].text.strip()

            if interest_method == "고정금리":
                interest_method = "FXD"
            elif interest_method == "변동금리":
                interest_method = "VAR"

            if repayment_method == "원리금분할상환":
                repayment_method = "EQP"
            elif repayment_method == "원금분할상환": 
                repayment_method = "CPA"
            elif repayment_method == "만기일시상환":
                repayment_method = "BUL"    

            # 상품 정보 출력 (디버깅 용)
            # print(f"은행: {bank_name}")
            # print(f"상품명: {product_name}")
            # print(f"금리방식: {interest_method}")
            # print(f"상환방식: {repayment_method}")
            # print(f"최저금리: {min_interest}")
            # print(f"최고금리: {max_interest}")

            # 결과를 product_list에 저장하고 싶다면, product_list에 append
            product_list.append({
                "bank_name": bank_name,
                "product_name": product_name,
                "residence_type": residence_type,
                "interest_method": interest_method,
                "repayment_method": repayment_method,
                "min_interest_rate": min_interest,
                "max_interest_rate": max_interest
            })

        print(f"대출 {residence_type} 조회 완료 | 상품 개수 : {len(product_list)}")
        return product_list

    except Exception as e:
        print(f"대출 {residence_type} 조회 오류 발생: {e}")
        return [{"ERROR": str(e)}]
    
if __name__ == "__main__":
    getLoanData('Interest1')
    getLoanData('Interest2')