# ISAC

* INTEGRATED SYSTEM FOR ANSWERING CUSTOMER JUSTICE USING NLP
* NLP를 통한 소비자 민원 자동 답변 시스템

<br>

### Homepage UI

---

![demo](/img/demo.png)<br>

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