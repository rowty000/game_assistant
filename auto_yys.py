# -*- coding: utf-8 -*-
# @Time : 2019/4/11 12:21
# @Author : Vanya
import time
import random
import pygame
from uiautomator import device as d
from judgement import Judgement


random.seed(time.time())
pygame.mixer.init()


def warning():
    track = pygame.mixer.Sound('Ring03_1.wav')
    track.play(loops=-1)
    input('input to stop')


def click_range(x, y):
    d.click(x + random.randint(-10, 10), y + random.randint(-10, 10))
    time.sleep(2)


def auto_challenge(times):
    judge = Judgement()
    pic_name = 'auto_challenge.png'
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
            for j in range(60):  # * 3 seconds
                d.screenshot(pic_name)
                time.sleep(3)
                if judge.is_reward_continue_page(pic_name):
                    print('win')
                    click_range(1200, 185)
                    break
                elif judge.is_failed(pic_name):
                    print('failed')
                    click_range(1200, 185)
                    break
            else:
                print(' not find stop reward ')
                warning()
                return
        except Exception as e:
            print(e)
            warning()
    warning()


def auto_yuhun(times):
    judge = Judgement()
    pic_name = 'auto_challenge.png'
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
            for j in range(60):
                d.screenshot(pic_name)
                time.sleep(3)
                if judge.is_reward_continue_page(pic_name):
                    print('win')
                    click_range(1200, 185)
                    break
                elif judge.is_failed(pic_name):
                    print('failed')
                    click_range(1200, 185)
                    break
            else:
                print(' not find stop reward ')
                warning()
                return
        except Exception as e:
            print(e)
            warning()
    warning()


if __name__ == '__main__':
    # auto_challenge(4)
    auto_yuhun(15)
