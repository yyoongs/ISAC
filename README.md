# ISAC
<img width="618" alt="Screen Shot 2023-04-07 at 4 45 23 PM" src="https://user-images.githubusercontent.com/48539539/230565926-29d4f951-1984-4830-9d68-5cdd70da8ad3.png" align=center>


<br>

### INTEGRATED SYSTEM FOR ANSWERING CUSTOMER JUSTICE USING NLP

---
#### NLP를 통한 소비자 민원 자동 답변 시스템
> 한국데이터산업진흥원 주관 빅데이터 청년인재 프로그램
> 
> 개발기간 : 2019.07 - 2019.08


### Teams
---
> 조용성
> 
> 곽기은
> 
> 박지영
> 
> 유원선
> 
> 김은경

### DEMO
---

<img width="611" alt="Screen Shot 2023-04-07 at 4 45 34 PM" src="https://user-images.githubusercontent.com/48539539/230568306-be2cb77f-a04f-4d46-97ed-1f9175df6ea1.png">
<img width="620" alt="Screen Shot 2023-04-07 at 4 45 43 PM" src="https://user-images.githubusercontent.com/48539539/230568322-d9c5e838-1162-497d-98a0-153e8e1d47d0.png">
<img width="591" alt="Screen Shot 2023-04-07 at 4 45 51 PM" src="https://user-images.githubusercontent.com/48539539/230568340-c440cbec-9f42-4b45-a14f-9a58ceeaed66.png">

### Stacks 기술스택
---
*BE 및 데이터 분석 :*   <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 

*FE :*   <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"> 



### Models
---
1. word2hybrid model
   * 입력한 제목을 기반으로 소비자민원센터에서 유사한 답변을 뽑아주는 모델
2. word2criteria model
   * 사용자가 입력한 민원에 대한 적절한 해결기준을 불러오는 모델
   * 민원에 대한 해결기준이 존재한다면 해결기준의 상세내용 출력
   * 해결기준이 없다면 존재하지 않음을 출력
3. word2judge model
   * 답변 생성을 위한 다양한 모델들의 집합
   * 소비자원에서 제공하는 답변의 구조대로 모델 생성 :  추가서류 여부, 소비자가 협상할 상황인지 여부, 소비자원에서 전화상으로 협상 권고를 하는 경우, 구제서류 제출을 요구하는 경우
   * 4가지 모델의 아웃풋의 조합으로 답변 템플릿 생성
<br>
