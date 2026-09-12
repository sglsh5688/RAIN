# LIBERO Analogy · Task 검수

[검수 페이지](index.html) · [Selected Tasks](../selected29/index.html) · [ID 대응표](ID_MAPPING.tsv)

새 ID를 사용하는 60개 task의 Task Description, 목표, 초기 scene, 행동 단계별 mask를 모았습니다. 카테고리별로 Decomposition_001–020, Adapt_001–020, Compose_001–020이며 이전 ID도 함께 표시합니다.

페이지에서 task와 단계를 선택한 뒤 Scene / Mask overlay / 이진 mask를 전환하세요. 별도 이동 목표가 있는 단계는 행동 대상과 목표 영역 mask를 나눠 볼 수 있습니다. 검수 상태와 메모는 브라우저에 저장되며, 내보내기를 누르면 전체60개 task의 검수 기록을 JSON으로 받을 수 있습니다. 이 기록은 자동으로 GitHub에 전송되지 않습니다.

모든 장면은 초기 상태0, seed7, 평가의10회 초기 안정화 control 직후입니다. 153개 행동 단계에 대해 RGB120장과 이진 mask444개를 저장했습니다. 13개 wrist mask는 이 초기 시야에서 보이지 않거나 투영할 수 없어 비어 있습니다. 다른 초기 배치나 행동 이후 장면은 포함하지 않습니다.

각 task의 `scenes/<Category>/<Task_ID>/TASK_REVIEW.png`에는 설명과 전체 단계 mask가 한 장으로 정리되어 있습니다. 카테고리 전체 보기: [Decomposition](overview/Decomposition.png), [Adapt](overview/Adapt.png), [Compose](overview/Compose.png).

영상은 완료된 RAIN 50episode 평가의 실제 성공59개·실패53개 대표 기록입니다. 이전 ID가 영상에 남아 있으며 대응표로 연결됩니다. 페이지의 성공률은 이50episode 평가 기준입니다. 과거 비교 이미지는 Selected Tasks 페이지에 있던 기존 자료입니다. 새로운 정책 추론이나 성공 영상의 추가 수동 인증은 수행하지 않았습니다.

공개 definition 파일은 task 의미와 판정 조건을 유지하며, 로컬 실행 경로는 `local-source:<filename>`로 표시했습니다. 현재 scene의 출처와 mask 정보는 task별 `scene.json`에 있습니다. [공개 자료 요약](REVIEW_SUMMARY.json), [영상 목록](VIDEO_INDEX.json), [한글 글꼴 라이선스](assets/NotoSans-LICENSE.txt)를 함께 제공합니다.

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
