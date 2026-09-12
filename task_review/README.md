# LIBERO Analogy · Task 검수

[검수 페이지](index.html) · [Selected Tasks](../selected29/index.html) · [ID 대응표](ID_MAPPING.tsv)

새 ID를 사용하는 60개 task의 Task Description, 목표, 초기 scene, 행동 단계별 mask를 모았습니다. 카테고리별로 Decomposition_001–020, Adapt_001–020, Compose_001–020이며 이전 ID도 함께 표시합니다.

페이지에서 task와 단계를 선택한 뒤 Scene / Mask overlay / 이진 mask를 전환하세요. 별도 이동 목표가 있는 단계는 행동 대상과 목표 영역 mask를 나눠 볼 수 있습니다. 검수 상태와 메모는 브라우저에 저장되며, 내보내기를 누르면 전체60개 task의 검수 기록을 JSON으로 받을 수 있습니다. 이 기록은 자동으로 GitHub에 전송되지 않습니다.

모든 장면은 초기 상태0, seed7, 평가의10회 초기 안정화 control 직후입니다. 153개 행동 단계에 대해 RGB120장과 이진 mask444개를 저장했습니다. 13개 wrist mask는 이 초기 시야에서 보이지 않거나 투영할 수 없어 비어 있습니다. 다른 초기 배치나 행동 이후 장면은 포함하지 않습니다.

각 task의 `scenes/<Category>/<Task_ID>/TASK_REVIEW.png`에는 설명과 전체 단계 mask가 한 장으로 정리되어 있습니다. 카테고리 전체 보기: [Decomposition](overview/Decomposition.png), [Adapt](overview/Adapt.png), [Compose](overview/Compose.png).

영상은 완료된 RAIN 50episode 평가의 실제 성공59개·실패53개 대표 기록입니다. 이전 ID가 영상에 남아 있으며 대응표로 연결됩니다. 페이지의 성공률은 이50episode 평가 기준입니다. 과거 비교 이미지는 Selected Tasks 페이지에 있던 기존 자료입니다. 새로운 정책 추론이나 성공 영상의 추가 수동 인증은 수행하지 않았습니다.

공개 definition 파일은 task 의미와 판정 조건을 유지하며, 로컬 실행 경로는 `local-source:<filename>`로 표시했습니다. 현재 scene의 출처와 mask 정보는 task별 `scene.json`에 있습니다. [공개 자료 요약](REVIEW_SUMMARY.json), [영상 목록](VIDEO_INDEX.json), [한글 글꼴 라이선스](assets/NotoSans-LICENSE.txt)를 함께 제공합니다.
