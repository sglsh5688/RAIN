## 현재 지시문 · 2026-09-12 업데이트

Decomposition·Adapt·Compose 총60개 현재 instruction에서 마침표를 모두 제거했습니다. 원본 LIBERO의130개 BDDL 지시문과 실제 benchmark Task.language는 모두 마침표 없이 끝납니다. 이전에 추가했던 Adapt_010–013의 마침표도 제거했습니다.

Adapt_009의 현재 지시문은 다음과 같습니다.

> Put the yellow and white mug in the right compartment of the caddy

여기서 right는 **로봇 베이스 기준 오른쪽 칸**입니다. Caddy가180° 회전되어 있으므로 그 칸의 내부 식별자는 원본 `desk_caddy_1_left_contain_region`입니다. 실제 목적지는 그대로 두고 지시문을 로봇 기준으로 수정했습니다. [좌표로 비교한 그림](COMPARTMENT_FRAMES.png)에서 물체의 구획 이름과 로봇 기준의 차이를 확인할 수 있습니다. 현재 RAIN mask는 caddy 전체를 표시하므로 특정 칸 하나의 mask로 읽으면 안 됩니다.

| Task | 현재 instruction의 목표 방향 |
|---|---|
| Adapt_009 | mug → caddy의 로봇 기준 오른쪽 칸 |
| Adapt_017 | alphabet soup → drainer 오른쪽 칸 |
| Compose_015 | butter → drainer 왼쪽 칸, tomato sauce → 오른쪽 칸 |
| Compose_018 | alphabet soup → drainer 오른쪽 칸, tomato sauce → 왼쪽 칸 |

세 drainer task는 물체 회전이0°이므로 원본 구획 이름과 로봇 베이스 기준 방향이 일치합니다. [Drainer 단계별 방향 비교](DRAINER_DIRECTIONS.png)는 현재 RAIN 화면 방향의 mask를 사용합니다. 과거 비교 이미지는 다른 화면 방향, mask 합성 또는 변경 전 문구를 포함할 수 있어 별도 링크로 표시했습니다.

Compose_019의 현재 지시문은 기존 동작 순서를 유지합니다.

> Put the alphabet soup in the basket, then put the butter in the basket, then put the cream cheese box in the basket

현재 목록·description·공개 definition·task 검수 이미지·카테고리 전체 이미지에 같은 지시문을 반영했습니다. [변경 이력](INSTRUCTION_REVISIONS.json)의 tasks는 최초 보존 패키지 대비 누적56개 변경이며, history는 이전 마침표 추가와 이번60개 제거/방향 수정 기록을 보존합니다. Adapt_010–013은 최초 문구와 다시 같아졌습니다.

기존 평가 영상·성공률·행동별 source description은 평가 당시 기록입니다. 물리 배치·원본 goal site·판정 조건·mask를 바꾸거나 정책 평가를 다시 실행하지 않았습니다. 원본 source/evaluation 기록의 마침표와 문구는 현재 instruction과 구분해서 보존합니다.

원본 근거: [caddy 구획 및180° 배치](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/8f1084e3132a39270c3a13ebe37270a43ece2a01/libero/libero/bddl_files/libero_90/STUDY_SCENE1_pick_up_the_book_and_place_it_in_the_left_compartment_of_the_caddy.bddl), [bowl-drainer 구획 XML](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/8f1084e3132a39270c3a13ebe37270a43ece2a01/libero/libero/assets/turbosquid_objects/bowl_drainer/bowl_drainer.xml)
