import random

def draw_old(cnt: int) -> bool:
    if random.random() <= 0.007:
        return True
    return False


def draw_new(cnt: int) -> bool:
    if cnt == 100:
        return random.random() <= 0.5
    return draw_old(cnt)


def draw_until_collected(max_count: int, newmode: bool) -> int:
    cnt = 0
    while cnt < max_count:
        cnt += 1
        if newmode:
            if draw_new(cnt):
                return cnt
        else:
            if draw_old(cnt):
                return cnt
    return -1


def draw_multi_pickup(character_count: int, newmode: bool) -> int:
    total_count = 0  # 总抽数
    point_count = 0  # 招募点数
    collected_character_count = 0  # 招募学生数量

    reset_flag: int = 0

    while True:

        # 假设旧机制每隔1个池重置点数
        # 重要！视情况注释此段
        # if not newmode:
        #     if collected_character_count % 2 == 0:
        #         point_count = 0

        if collected_character_count >= character_count:
            break

        max_count = 200 - point_count

        result = draw_until_collected(max_count, newmode)

        if result == -1:
            result = max_count
        else:
            collected_character_count += 1

        if point_count + result >= 200:
            assert point_count + result <= 200
            total_count += 200 - point_count
            point_count = 0
            collected_character_count += 1
            continue

        if newmode:
            point_count = 0
        else:
            point_count += result

        total_count += result

    return total_count