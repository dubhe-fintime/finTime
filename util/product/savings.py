import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 은행연합회 적금 상품 조회
# 방식 : API
# 수집 데이터
##############################

##############################
# Service URL = "https://portal.kfb.or.kr/compare/receiving_neosave_search_result_new2.php"
# Method = POST
##############################

async def getSavingsData(InterestType):
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    product_list = []
    # API URL
    url =  "https://portal.kfb.or.kr/compare/receiving_neosave_search_result_new2.php"
    ######### 기초 설정 END ##############

    strInterestType = ""
    saving_method = ""
    intr_calc = ""

    if InterestType == "Simple1":
        strInterestType = "정액적립식 단리"
        saving_method = "SM02"
        intr_calc = "INTR01"
    elif InterestType == "Simple2":
        strInterestType = "자유적립식 단리"
        saving_method = "SM03"
        intr_calc = "INTR01"
    elif InterestType == "Compound1":
        strInterestType = "정액적립식 복리"
        saving_method = "SM02"
        intr_calc = "INTR02"
    elif InterestType == "Compound2":
        strInterestType = "자유적립식 복리"
        saving_method = "SM03"
        intr_calc = "INTR02"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        body = {
            "InterestType": InterestType,
            "BankValue": "0010030|0013175|0011625|0010001|0010002|0013909|0010026|0010927|0010006|0014807|0010016|0010017|0010019|0010020|0010022|0010024|0014674|0015130|0017801",
            "InterestMonth": "BANK_ORDER",
            "OrderByType": "ASC",
            "JOIN_METHOD": "",
            "EXPIRATION": "2",
            "SortType": ""
        }

        # 웹페이지 요청
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, "html.parser")

        div_tag = soup.find_all("div")[1]
        products = div_tag.find_all("tr")

        if 'th' in str(products[0]):
            products = products[1:]

        products = [product for product in products if product.get('id') != 'Goods_Text_TR']

        # 검색결과가 없을 때
        no_results = False

        # 검색결과가 없다는 텍스트가 있는 tr 태그가 있는지 확인
        for product in products:
            if "검색결과가 없습니다." in product.text:
                no_results = True
                break

        if no_results:
            print(f"적금 {strInterestType} 완료 | 결과 없음")
            return product_list
        
        for product in products:
            # 첫 번째 td에서 은행 이름 추출
            bank_name = product.find_all("td")[0].text.strip()

            # 두 번째 td에서 상품 이름과 링크 추출
            product_name = product.find_all("td")[1].find("a").text.strip()
            product_link = product.find_all("td")[1].find("a")["href"]

            # 세 번째 td에서 기본금리 추출
            basic_interest_rate = product.find_all("td")[2].text.strip()

            # 네 번째 td에서 최고금리 추출
            max_interest_rate = product.find_all("td")[3].text.strip()

            # 마지막 td에서 전월취급 평균금리 추출
            average_interest_rate = product.find_all("td")[5].text.strip()

            # 추출한 데이터 출력
            #print(f"은행 이름: {bank_name}")
            #print(f"상품 이름: {product_name}")
            #print(f"상품 링크: {product_link}")
            #print(f"기본금리: {basic_interest_rate}")
            #print(f"최고금리: {max_interest_rate}")
            #print(f"전월취급 평균금리: {average_interest_rate}")

            # 결과를 product_list에 저장하고 싶다면, product_list에 append
            product_list.append({
                "prod_type": "PROD02",
                "saving_method": saving_method,
                "intr_calc": intr_calc,
                "bank_name": bank_name,
                "product_name": product_name,
                "product_link": product_link,
                "basic_interest_rate": basic_interest_rate,
                "max_interest_rate": max_interest_rate,
                "average_interest_rate": average_interest_rate
            })

        print(f"적금 {strInterestType} 완료 | 상품 개수 : {len(product_list)}")
        return product_list

    except Exception as e:
        print(f"적금 {strInterestType} 오류 발생: {e}")
        return [{"ERROR": str(e)}]