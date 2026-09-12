## 2026-09-12 설명·방향 확인

Adapt_010, Adapt_011, Adapt_012, Adapt_013의 Task Description 끝에 마침표를 추가했습니다. Compose_019는 LIBERO의 “put … in the basket” 표현을 사용해 각 동작의 순서를 명시했습니다.

> Put the alphabet soup in the basket, then put the butter in the basket, then put the cream cheese box in the basket.

LIBERO 원본 [bowl drainer XML](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/8f1084e3132a39270c3a13ebe37270a43ece2a01/libero/libero/assets/turbosquid_objects/bowl_drainer/bowl_drainer.xml)의 구획 이름과 위치를 확인했습니다. 로봇 기준 왼쪽 구획은 `left_region`(로컬 +Y), 오른쪽 구획은 `right_region`(로컬 −Y)입니다. 세 task 모두 구획 방향과 목표가 일치합니다.

| Task | 동작 순서 |
|---|---|
| Adapt_017 | alphabet soup → 오른쪽 구획 |
| Compose_015 | butter → 왼쪽 구획, tomato sauce → 오른쪽 구획 |
| Compose_018 | alphabet soup → 오른쪽 구획, tomato sauce → 왼쪽 구획 |

세 task의 현재 검수 화면과 Selected Tasks의 기본 비교 이미지는 같은 RAIN 화면 방향을 사용합니다. [구획 방향 비교](DRAINER_DIRECTIONS.png)에서 단계별 목표 mask를 확인할 수 있습니다. Adapt_017·Compose_018의 과거 비교 이미지는 현재 화면과 좌우 표시 방향이 다르고, Compose_015의 과거 이미지는 두 구획의 mask를 합쳐 표시합니다. 이들은 과거 자료로 따로 표시했습니다.

표현은 모두 “the left/right compartment of the bowl drainer” 형식으로 일치합니다. Compose_019의 “cream cheese box” 명칭은 원본 [LIBERO-10 task 목록](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/bddl_files/libero_10/tasks_info.txt)을 따릅니다. 이 합성 task의 세 동작 순서는 기존 목표 순서와 같습니다.

수정 이력은 [INSTRUCTION_REVISIONS.json](INSTRUCTION_REVISIONS.json)에 있습니다. 배치·목표 순서·판정 조건·mask는 그대로이며 정책 평가를 다시 실행하지 않았습니다. 표시된 성공률과 영상은 수정 전 문장으로 완료된 50episode 평가 기록입니다. 수정 task의 영상 영역에 당시 문장을 함께 표시하며, 행동별 source description도 유지합니다.
