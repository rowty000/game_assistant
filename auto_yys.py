# -*- coding: utf-8 -*-
# @Time : 2019/4/11 12:21
# @Author : Vanya
import time
import math
import traceback
import random
import pygame
from uiautomator import device as d
from judgement import Judgement


random.seed(time.time())
pygame.mixer.init()
judge = Judgement()
pic_name = 'auto_challenge.png'


def warning():
    track = pygame.mixer.Sound('Ring03_1.wav')
    track.play(loops=-1)
    input('input to stop')


def click_range(x, y):
    d.click(x + random.randint(-10, 10), y + random.randint(-10, 10))
    time.sleep(2)


def wait_for_end():
    for j in range(60):  # * 3 seconds
        d.screenshot(pic_name)
        time.sleep(3)
        if judge.is_reward_continue_page(pic_name):
            print('win')
            click_range(1200, 185)
            return True
        elif judge.is_failed(pic_name):
            print('failed')
            click_range(1200, 185)
            return True
    else:
        print(' not find stop reward ')


def auto_challenge(times):
    refresh_times = 0
    for i in range(times):
        try:
            print('times', i+1)
            time.sleep(2)
            d.screenshot(pic_name)
            print('check reward')
            if judge.is_reward_continue_page(pic_name):
                print('get reward for count')
                click_range(650, 570)
                d.screenshot(pic_name)
            print('find challenge')
            pos = judge.find_can_challenge_pos(pic_name)
            if not pos:
                print('can not get challenge pos')
                if refresh_times == 0:
                    print('refresh')
                    click_range(1180, 600)
                    d.screenshot(pic_name)
                    print('find refresh ok')
                    if judge.is_refresh_ok(pic_name):
                        click_range(850, 500)
                    else:
                        warning()
                        return
                    refresh_times = 1
                    continue
                warning()
                return
            refresh_times = 0
            print('pos is ', pos)
            top, right = pos
            click_range(right-40, top+40)
            d.screenshot(pic_name)
            print('find challenge in')
            if not judge.is_challenge_in_page(pic_name, top, right):
                print('not challenge in page')
                warning()
                return
            click_range(right-128, top+295)
            print('challenge in')
            if not wait_for_end():
                warning()
                return
        except Exception as e:
            print(traceback.format_stack(e))
            warning()
    warning()


def auto_yuhun(times):
    for i in range(times):
        try:
            print('times', i+1)
            time.sleep(2)
            d.screenshot(pic_name)
            print('find challenge in')
            if not judge.is_yuhun_challenge_in_page(pic_name):
                print('not challenge in page')
                warning()
                return
            click_range(1041, 578)
            print('challenge in')
            if not wait_for_end():
                warning()
                return
        except Exception as e:
            print(traceback.format_stack(e))
            warning()
    warning()


def attack_boss(pos):
    click_range(pos[0], pos[1])
    if not wait_for_end():
        warning()
        return
    box_time = 0
    while True:
        time.sleep(2)
        d.screenshot(pic_name)
        print('find box')
        pos = judge.get_boss_box_pos(pic_name)
        if not pos:
            print('no box', box_time)
            if box_time < 5:
                box_time += 1
                continue
            break
        print('get box')
        click_range(pos[0], pos[1])
        click_range(1200, 175)
    return True


def auto_tansuo(times):
    first_start = True
    count = 0
    while True:
        try:
            d.screenshot(pic_name)
            print('find entry')
            if not judge.is_exploration_in_page(pic_name):
                print('not entry page')
                if not first_start:
                    warning()
                    return
            else:
                click_range(1066, 604)
                print('entry')
            first_start = False
            move_times = 0
            while True:
                d.screenshot(pic_name)
                print('find boss')
                pos = judge.get_attack_boss_pos(pic_name)
                if pos:
                    print('challenge in boss')
                    if not attack_boss(pos):
                        return
                    count += 1
                    if count == times:  # finish
                        warning()
                        return
                    break
                print('no boss, find goblin')
                pos = judge.get_attack_pos(pic_name)
                if pos:
                    click_range(pos[0], pos[1])
                    print('challenge in goblin')
                    if not wait_for_end():
                        warning()
                        return
                    count += 1
                    if count == times:  # finish
                        warning()
                        return
                    continue
                print('no goblin')
                if move_times < 3:
                    print('move right', move_times)
                    click_range(1300, 570)  # right
                elif move_times < 6:
                    print('move left', move_times)
                    click_range(100, 570)  # left
                else:
                    print('move back no boss')
                    warning()
                    return
                move_times += 1
                time.sleep(3)

        except Exception as e:
            print(traceback.format_stack(e))
            warning()


def get_experience_goblin():
    pos = judge.get_attack_pos(pic_name)
    if not pos:
        return
    for i in range(6):
        print('find experience pos', i, time.time())
        pos = judge.get_experience_pos(pic_name)
        if not pos:
            print('not found')
            time.sleep(0.5)
            d.screenshot(pic_name)
            continue
        search_box = (pos[0] - 300, pos[1] - 300, pos[0] + 300, pos[1])
        im = judge.get_crop_pic(pic_name, search_box)
        print('find attack pos', time.time())
        pos_list = judge.get_attack_pos(im, all_pos=True, pic_as_img=True)
        if not pos_list:
            print('not found')
            return
        print('find nearest', time.time())
        pos_list = [(x[0] + pos[0] - 200, x[1] + pos[1] - 300) for x in pos_list]
        min_dis = 100000000000
        min_pos = None
        for apos in pos_list:
            dis = math.sqrt((apos[0] - pos[0]) ** 2 + (apos[1] - pos[1]) ** 2)
            if dis < min_dis:
                min_pos = apos
                min_dis = dis
        if not min_pos:
            return
        print('find attack again', time.time())
        pos = min_pos
        d.screenshot(pic_name)
        im = judge.get_crop_pic(pic_name, [pos[0]-250, pos[1]-250, pos[0]+250, pos[1]+250])
        pos_list = judge.get_attack_pos(im, all_pos=True, pic_as_img=True)
        if not pos_list:
            print('not found')
            return
        print('find nearest', time.time())
        pos_list = [(x[0] + pos[0] - 250, x[1] + pos[1] - 250) for x in pos_list]
        min_dis = 100000000000
        min_pos = None
        for apos in pos_list:
            dis = math.sqrt((apos[0] - pos[0]) ** 2 + (apos[1] - pos[1]) ** 2)
            if dis < min_dis:
                min_pos = apos
                min_dis = dis
        if not min_pos:
            return
        print('attack pos', min_pos, time.time())
        return min_pos[0], min_pos[1]


def get_no_attack_pos_x(x_start, x_end, pos_y):
    band = (min(x_start, x_end)-70, pos_y-140, max(x_start, x_end)+70, pos_y + 140)
    im = judge.get_crop_pic(pic_name, band)
    pos_list = judge.get_attack_pos(im, all_pos=True, pic_as_img=True)
    if not pos_list:
        return x_start
    pos_x_list = [x[0] for x in pos_list]
    safe_sections = [[min(x_start, x_end), max(x_start, x_end)]]
    for pos_x in pos_x_list:
        pos_x_1 = pos_x - 100
        pos_x_2 = pos_x + 100
        new_safe_sections = []
        for section in safe_sections:
            if pos_x_1 > section[1] or pos_x_2 < section[0]:  # no intersection
                new_safe_sections.append(section)
                continue
            if pos_x_1 > section[0]:
                new_safe_sections.append([section[0], pos_x_1])
            if pos_x_2 < section[1]:
                new_safe_sections.append([pos_x_2, section[1]])
        safe_sections = new_safe_sections
    if x_start < x_end:
        return min([x[0] for x in safe_sections])
    else:
        return max([x[1] for x in safe_sections])


def quit_tansuo():
    if not judge.is_quit_page(pic_name):
        warning()
        return
    click_range(50, 70)
    d.screenshot(pic_name)
    if not judge.is_quit_ok_page(pic_name):
        warning()
        return
    click_range(850, 450)
    time.sleep(2)
    return True


def auto_tansuo_experience(times):
    first_start = True
    count = 0
    while True:
        try:
            d.screenshot(pic_name)
            print('find entry')
            if not judge.is_exploration_in_page(pic_name):
                print('not entry page')
                if not first_start:
                    warning()
                    return
            else:
                click_range(1066, 604)
                print('entry')
            first_start = False
            move_times = 0
            while True:
                d.screenshot(pic_name)
                print('find boss')
                pos = judge.get_attack_boss_pos(pic_name)
                if pos:
                    print('challenge in boss')
                    if not attack_boss(pos):
                        return
                    count += 1
                    print('count', count)
                    if count == times:  # finish
                        warning()
                        return
                    break
                print('no boss, find experience goblin')
                pos = get_experience_goblin()
                if pos:
                    print('challenge in goblin')
                    click_range(pos[0], pos[1])
                    if not wait_for_end():
                        warning()
                        return
                    count += 1
                    print('count', count)
                    if count == times:  # finish
                        warning()
                        return
                    continue
                print('no goblin')
                if move_times < 3:
                    pos_x = get_no_attack_pos_x(1300, 100, 570)
                    print('move right', move_times, pos_x)
                    click_range(pos_x, 570)  # right
                elif move_times < 6:
                    pos_x = get_no_attack_pos_x(100, 1300, 570)
                    print('move left', move_times, pos_x)
                    click_range(pos_x, 570)  # left
                else:
                    if quit_tansuo():
                        break
                    warning()
                    return
                move_times += 1
                time.sleep(3)

        except Exception as e:
            print(traceback.format_stack(e))
            warning()


if __name__ == '__main__':
    # auto_challenge(15)
    # auto_yuhun(15)
    auto_tansuo(15)
    # auto_tansuo_experience(20)
