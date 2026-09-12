# Compose_018

Legacy ID: `BDRMIN_002`

## Task Description

Pick the alphabet soup and place it in the right compartment of the bowl drainer, then pick the tomato sauce and place it in the left compartment of the bowl drainer.

## 목표

- in(alphabet_soup_1, bowl_drainer_1_right_region)
- in(tomato_sauce_1, bowl_drainer_1_left_region)

## 금지 목표

없음

## Scene / mask

초기 상태 index 0, seed 7. 모든 단계의 mask는 같은 초기 scene에서 표시합니다. 이후 로봇 행동의 진행 장면이 아닙니다.

[단계별 mask 검수 화면](../../../index.html#Compose_018)

[Scene 기록 및 이미지 경로](scene.json)

## Bowl drainer 방향

방향은 LIBERO 원본 구획 기준입니다. 로봇 기준 왼쪽은 left_region(+Y), 오른쪽은 right_region(−Y)입니다. 현재 scene과 단계별 mask는 같은 화면 방향을 사용합니다.

[세 task 방향 비교](../../../DRAINER_DIRECTIONS.png)
