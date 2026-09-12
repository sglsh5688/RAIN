# Compose_018

Legacy ID: `BDRMIN_002`

## Task Description

Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the tomato sauce and place it in the right compartment of the bowl drainer

## 목표

- in(alphabet_soup_1, bowl_drainer_1_right_region)
- in(tomato_sauce_1, bowl_drainer_1_left_region)

## 금지 목표

없음

## Scene / mask

초기 상태 index 0, seed 7. 모든 단계의 mask는 같은 초기 scene에서 표시합니다. 이후 로봇 행동의 진행 장면이 아닙니다.

[단계별 mask 검수 화면](../../../index.html#Compose_018)

[Scene 기록 및 이미지 경로](scene.json)

## Compartment 방향

현재 지시문은 로봇 팔 관점의 왼쪽→오른쪽 순서입니다. 수프의 left compartment는 내부 right_region, 토마토소스의 right compartment는 내부 left_region에 대응합니다. 실제 목적지와 mask는 그대로이며, 기존 평가·행동별 source 문구는 당시 기록입니다.

[현재 지시문 · 원본 구획 비교](../../../DRAINER_DIRECTIONS.png)
