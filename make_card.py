# This script is PDF related processing code

import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import read_data
import PIL

from reportlab.pdfbase import pdfmetrics,ttfonts
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
import os

A4_HEIGHT = 21 * cm
A4_WIDTH = 29.7 * cm
CARD_HEIGHT = 8.7 * cm
CARD_WIDTH = 5.7 * cm

A4_HEIGHT_HOR = 29.7 * cm
A4_WIDTH_HOR = 21 * cm
CARD_HEIGHT_HOR = 5.7 * cm
CARD_WIDTH_HOR = 8.7 * cm

POWER_MOON = 'powermoon.png'
MULTI_MOON = 'multimoon.png'
COMMUNITY = 'powermoon.png'
COMMUNITY_BACK = 'community_back.jpg'
CHANCE = 'chance.png'
CHANCE_BACK = 'chance_back.jpg'



def init():
    # create invoice folder
    card_path = 'cards/'
    if not os.path.exists(card_path):
        print('Create cards folder %s.', card_path)
        os.mkdir(card_path)
    add_chinese_font()

    im = PIL.Image.open(MULTI_MOON)
    x, y = im.size
    try:
        # 使用白色来填充背景
        # (alpha band as paste mask).
        p = PIL.Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        p.save(MULTI_MOON)
    except:
        pass

    im = PIL.Image.open(CHANCE)
    x, y = im.size
    try:
        # 使用白色来填充背景
        # (alpha band as paste mask).
        p = PIL.Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        p.save(CHANCE)
    except:
        pass


def get_cards_positions():

    x_start = (A4_WIDTH - 5 * CARD_WIDTH) / 2
    widths = [ x_start + CARD_WIDTH * i  for i in range(5)]
    heights = [A4_HEIGHT / 2, A4_HEIGHT / 2 - CARD_HEIGHT]
    result = []
    for width in widths:
        for height in heights:
            result.append((width, height))
    return result


def get_cards_positions_horizontal():

    x_start = (A4_WIDTH_HOR - 2 * CARD_WIDTH_HOR) / 2
    widths = [ x_start + CARD_WIDTH_HOR * i  for i in range(2)]
    y_start = (A4_HEIGHT_HOR - 5 * CARD_HEIGHT_HOR) / 2
    heights = [ y_start + CARD_HEIGHT_HOR * i  for i in range(5)]
    result = []
    for width in widths:
        for height in heights:
            result.append((width, height))
    return result


def create_property_cards():

    properties = read_data.get_sheet('Sheet1')
    positions = get_cards_positions()
    c = canvas.Canvas('cards/property_cards.pdf', pagesize=landscape(reportlab.lib.pagesizes.A4))
    cnt = 0

    for property in properties:
        pos = positions[cnt]
        draw_card_front(c, property, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    cnt = 0
    for property in properties:
        pos = positions[cnt]
        draw_card_back(c, property, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    c.save()


def draw_card_back(c, property, pos):
    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)
    c.rect(pos[0], pos[1], CARD_WIDTH, CARD_HEIGHT)

    padding_1 = 0.35 * cm
    padding_2 = 0.1 * cm

    c.setDash(3, 0)
    c.setStrokeColor(reportlab.lib.colors.black)
    c.rect(pos[0] + padding_1, pos[1] + padding_1, CARD_WIDTH - 2 * padding_1, CARD_HEIGHT - 2 * padding_1)

    c.setStrokeColor(property['color'])
    c.rect(pos[0] + padding_1 + padding_2, pos[1] + padding_1 + padding_2,
           CARD_WIDTH - 2 * ( padding_1 + padding_2), CARD_HEIGHT - 2 * ( padding_1 + padding_2))

    horizontal_middle = pos[0] + CARD_WIDTH / 2
    y = pos[1] + CARD_HEIGHT - padding_1 - padding_2 - 1.2 * cm

    c.setFillColor(reportlab.lib.colors.black)
    c.setFont("c-yaheibold", 13)
    name = property['chinese_name'].upper()
    if ' ' in name:
        names = name.split()
        c.drawCentredString(horizontal_middle, y, names[0])
        c.drawCentredString(horizontal_middle, y - 0.5 * cm, names[1])

    else:
        c.drawCentredString(horizontal_middle, y, name)

    y -= 1.8 * cm
    c.setFont("c-yaheibold", 10)
    c.drawCentredString(horizontal_middle, y, '抵押价值')

    y -= 0.4 * cm
    c.drawCentredString(horizontal_middle, y, 'MORTGAGE')
    y -= 0.3 * cm
    c.drawCentredString(horizontal_middle, y, 'VALUE $' + property['Mortgage'])

    y -= 0.6 * cm
    c.drawCentredString(horizontal_middle, y, '赎回需支付')
    y -= 0.4 * cm
    c.drawCentredString(horizontal_middle, y, 'PAY $' + property['unmortgage'])

    y -= 1.8 * cm
    c.setFont("c-yahei", 7)
    c.drawCentredString(horizontal_middle, y, '抵押地产时将此面向上')
    y -= 0.3 * cm
    c.drawCentredString(horizontal_middle, y, 'Card must be turned this side up')
    y -= 0.25 * cm
    c.drawCentredString(horizontal_middle, y, 'if property is mortgaged.')



def draw_card_front(c, property, pos):

    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)
    c.rect(pos[0], pos[1], CARD_WIDTH, CARD_HEIGHT)

    padding_1 = 0.35 * cm
    padding_2 = 0.1 * cm

    c.setStrokeColor(reportlab.lib.colors.black)
    c.setDash(3, 0)
    c.rect(pos[0] + padding_1, pos[1] + padding_1, CARD_WIDTH - 2 * padding_1, CARD_HEIGHT - 2 * padding_1)

    horizontal_middle = pos[0] + CARD_WIDTH / 2
    x = pos[0] + padding_1 + padding_2
    y = pos[1] + CARD_HEIGHT - padding_1 - padding_2

    c.setFillColor(property['color'])

    rect_height = 1.5 * cm
    c.rect(x, y - rect_height, CARD_WIDTH - 2 * padding_1 - 2 * padding_2, rect_height, fill=1)

    c.setFillColor(reportlab.lib.colors.black)
    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(2, 1)

    y -= 0.4 * cm
    c.setFont("c-yaheibold", 10)
    c.drawCentredString(horizontal_middle, y, '契约书 TITLE DEED')

    y -= 0.8 * cm
    c.setFont("c-yaheibold", 11)
    c.drawCentredString(horizontal_middle, y, property['chinese_name'].upper())

    x_left = x + 0.2 * cm
    x_right = pos[0] + CARD_WIDTH - padding_1 - padding_2 - 0.2 * cm
    img_x = x_right - 1.5 * cm
    img_size = 0.4 * cm

    y = pos[1] + CARD_HEIGHT - padding_1 - padding_2 - rect_height - 0.5 * cm
    c.setFont("c-yaheibold", 13)
    c.drawString(x_left, y, '土地租值Rent')

    c.setFont("c-yahei", 10)
    c.drawRightString(x_right, y, '$ '+property['rent_base'])

    font_size_1 = 8
    font_size_2 = 5
    font_size_3 = 8

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '持有同色系所有土地')

    y -= 0.2 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'Rent with colour set')

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['rent_all'])

    c.line(x_left, y - 0.1 * cm, x_right, y - 0.1 * cm)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '有一个能量月亮')

    y -= 0.2 * cm
    c.setFont("c-yahei",font_size_2)
    c.drawString(x_left, y, 'Rent with one Power Moon')

    c.drawInlineImage(POWER_MOON, img_x, y, width=img_size, height=img_size)

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['rent_1'])

    c.line(x_left, y - 0.1 * cm, x_right, y - 0.1 * cm)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '有两个能量月亮')

    y -= 0.2 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'Rent with two Power Moons')

    c.drawInlineImage(POWER_MOON, img_x, y, width=img_size, height=img_size)

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['rent_2'])

    c.line(x_left, y - 0.1 * cm, x_right, y - 0.1 * cm)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '有三个能量月亮')

    y -= 0.2 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'Rent with three Power Moons')

    c.drawInlineImage(POWER_MOON, img_x, y, width=img_size, height=img_size)

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['rent_3'])

    c.line(x_left, y - 0.1 * cm, x_right, y - 0.1 * cm)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '有四个能量月亮')

    y -= 0.2 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'Rent with four Power Moons')

    c.drawInlineImage(POWER_MOON, img_x, y, width=img_size, height=img_size)

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['rent_4'])

    c.line(x_left, y - 0.1 * cm, x_right, y - 0.1 * cm)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '有超级月亮')

    y -= 0.2 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'Rent with Multi Moon')

    c.drawInlineImage(MULTI_MOON, img_x, y, width=img_size, height=img_size)

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['rent_h'])

    c.setDash(2, 0)
    c.setStrokeColor(reportlab.lib.colors.black)
    c.line(x_left, y - 0.1 * cm, x_right, y - 0.1 * cm)
    c.setDash(2, 1)
    c.setStrokeColor(reportlab.lib.colors.lightgrey)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '建造能量月亮成本')

    y -= 0.2 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'Power Moon cost')

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['house_cost'])

    c.line(x_left, y - 0.1 * cm, x_right, y - 0.1 * cm)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '建造超级月亮成本')

    y -= 0.2 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'Multi Moon cost')

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + property['hotel_cost'])


# To support Chinese display, add Chinese font
def add_chinese_font():
    pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('c-yahei', 'Yahei.ttf'))
    pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('c-yaheibold', 'YaheiBold.ttf'))


def create_service_cards():
    services = read_data.get_sheet('Sheet2')
    positions = get_cards_positions()
    c = canvas.Canvas('cards/service_cards.pdf', pagesize=landscape(reportlab.lib.pagesizes.A4))
    cnt = 0

    for service in services:
        pos = positions[cnt]
        draw_service_card_front(c, service, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    cnt = 0
    for service in services:
        pos = positions[cnt]
        draw_card_back(c, service, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    c.save()


def draw_service_card_front(c, service, pos):
    if service['Type'] == 'Avatar':
        draw_avatar_card_front(c, service, pos)
    else:
        draw_transport_card_front(c, service, pos)


def draw_avatar_card_front(c, service, pos):

    im = PIL.Image.open(service['img'])
    x, y = im.size
    try:
        # 使用白色来填充背景
        # (alpha band as paste mask).
        p = PIL.Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        p.save(service['img'])
    except:
        pass

    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)
    c.rect(pos[0], pos[1], CARD_WIDTH, CARD_HEIGHT)

    padding = 0.3 * cm

    c.setStrokeColor(reportlab.lib.colors.black)
    c.setDash(3, 0)
    c.rect(pos[0] + padding, pos[1] + padding, CARD_WIDTH - 2 * padding, CARD_HEIGHT - 2 * padding)

    horizontal_middle = pos[0] + CARD_WIDTH / 2
    x_left = pos[0] + 2 * padding
    x_right = pos[0] + CARD_WIDTH - 2 * padding
    y = pos[1] + CARD_HEIGHT - padding - 3.4 * cm

    # c.setFillColor(reportlab.lib.colors.black)
    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(2, 1)

    img_size = 3 * cm
    c.drawInlineImage(service['img'], horizontal_middle - img_size / 2, y, width=img_size, height=img_size)

    avatar_name = service['chinese_name'].upper()
    c.setFont("c-yaheibold", 15)
    y -= 0.6 * cm
    c.drawCentredString(horizontal_middle, y, 'MARIO')
    y -= 0.5 * cm
    c.drawCentredString(horizontal_middle, y, avatar_name[6:])

    y -= 0.3 * cm
    c.line(x_left, y, x_right, y)

    y -= 0.7 * cm

    c.setFont("c-yaheibold", 13)
    c.drawString(x_left, y, '租值Rent')

    c.setFont("c-yahei", 10)
    c.drawRightString(x_right, y, '$ '+service['Single'])

    y -= 0.1 * cm
    c.line(x_left, y, x_right, y)

    font_size_1 = 8
    font_size_2 = 6
    font_size_3 = 8

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '拥有2个替身')

    y -= 0.25 * cm
    c.setFont("c-yahei",font_size_2)
    c.drawString(x_left, y, 'If 2 avatars are owned')

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + service['two'])

    y -= 0.1 * cm
    c.line(x_left, y, x_right, y)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '拥有3个替身')

    y -= 0.25 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'If 3 avatars are owned')

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + service['three'])

    y -= 0.1 * cm
    c.line(x_left, y, x_right, y)

    y -= 0.45 * cm
    c.setFont("c-yahei", font_size_1)
    c.drawString(x_left, y, '拥有4个替身')

    y -= 0.25 * cm
    c.setFont("c-yahei", font_size_2)
    c.drawString(x_left, y, 'If 4 avatars are owned')

    c.setFont("c-yahei", font_size_3)
    c.drawRightString(x_right, y + 0.1 * cm, '$ ' + service['four'])


def draw_transport_card_front(c, service, pos):

    im = PIL.Image.open(service['img'])
    x, y = im.size
    try:
        # 使用白色来填充背景
        # (alpha band as paste mask).
        p = PIL.Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        p.save(service['img'])
    except:
        pass

    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)
    c.rect(pos[0], pos[1], CARD_WIDTH, CARD_HEIGHT)

    padding = 0.3 * cm

    c.setStrokeColor(service['color'])
    c.setDash(3, 0)
    c.rect(pos[0] + padding, pos[1] + padding, CARD_WIDTH - 2 * padding, CARD_HEIGHT - 2 * padding)

    horizontal_middle = pos[0] + CARD_WIDTH / 2
    x_left = pos[0] + 2 * padding
    x_right = pos[0] + CARD_WIDTH - 2 * padding
    y = pos[1] + CARD_HEIGHT - padding - 3.4 * cm

    # c.setFillColor(reportlab.lib.colors.black)
    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(2, 1)

    img_size = 3 * cm
    c.drawInlineImage(service['img'], horizontal_middle - img_size / 2, y, width=img_size, height=img_size)

    name = service['chinese_name'].upper()
    c.setFont("c-yaheibold", 15)
    y -= 1 * cm
    c.drawCentredString(horizontal_middle, y, name)

    y -= 0.3 * cm
    c.line(x_left, y, x_right, y)

    c.setFont("c-yahei", 7)
    linespace = 0.3 * cm

    y -= 0.4 * cm
    c.drawCentredString(horizontal_middle, y, '拥有一个交通工具时，')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, '其租值为掷出点数的4倍。*')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, '拥有两个交通工具时，')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, '其租值为掷出点数的10倍。*')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, '*乘10,000倍')

    y -= 0.4 * cm
    c.drawCentredString(horizontal_middle, y, 'If one "Transport" is owned, rent is')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, '4 times amount shown on dice. *')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, 'If two "Transports" is owned, rent is')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, '10 times amount shown on dice. *')
    y -= linespace
    c.drawCentredString(horizontal_middle, y, '*Multiplied by 10,000')



def create_community_cards():
    cards = read_data.get_sheet('Community')
    positions = get_cards_positions_horizontal()
    c = canvas.Canvas('cards/community_cards.pdf', pagesize = reportlab.lib.pagesizes.A4)
    cnt = 0

    for card in cards:
        pos = positions[cnt]
        draw_community_card_front(c, card, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    cnt = 0
    for i in range(len(cards)):
        pos = positions[cnt]
        draw_community_card_back(c, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    c.save()


def draw_community_card_front(c, card, pos):

    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)
    c.rect(pos[0], pos[1], CARD_WIDTH_HOR, CARD_HEIGHT_HOR)

    padding = 0.3 * cm

    c.setStrokeColor(reportlab.lib.colors.black)
    c.setDash(3, 0)
    c.rect(pos[0] + padding, pos[1] + padding, CARD_WIDTH_HOR - 2 * padding, CARD_HEIGHT_HOR - 2 * padding)

    horizontal_middle = pos[0] + CARD_WIDTH_HOR / 2
    x_left = pos[0] + 2 * padding
    x_right = pos[0] + CARD_WIDTH_HOR - 2 * padding
    y = pos[1] + CARD_HEIGHT_HOR - padding - 0.8 * cm

    # c.setFillColor(reportlab.lib.colors.black)
    # c.setStrokeColor(reportlab.lib.colors.lightgrey)
    # c.setDash(2, 1)

    c.setFont("c-yaheibold", 15)
    c.drawCentredString(horizontal_middle, y, '月亮福利  POWER MOON')

    img_size = 2.5 * cm
    y -=  img_size + 0.1 * cm
    c.drawInlineImage(COMMUNITY, x_left + 0.5 * cm, y, width=img_size, height=img_size)

    c.setFont("c-yahei", 8)
    x_chinese = (x_left + img_size + 0.5 * cm + x_right) / 2
    y += img_size - 1 * cm

    for i in range(3):
        title = 'Chinese_' + str(i+1)
        sentence = card[title].upper()
        c.drawCentredString(x_chinese, y, sentence)
        y -= 0.5 * cm

    y = pos[1] + CARD_HEIGHT_HOR - padding - 3.7 * cm
    x_english = (x_left + x_right) / 2

    for i in range(3):
        title = 'English_' + str(i+1)
        sentence = card[title].upper()
        c.drawCentredString(x_english, y, sentence)
        y -= 0.3 * cm

    y = pos[1] + CARD_HEIGHT_HOR - padding - 5 * cm
    c.setFont("c-yahei", 6)
    c.drawCentredString(x_english, y, '16 - ' + str(int(card['Index']) ))



def draw_community_card_back(c, pos):
    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)

    c.drawInlineImage(COMMUNITY_BACK, pos[0], pos[1], width=CARD_WIDTH_HOR, height=CARD_HEIGHT_HOR)
    c.rect(pos[0], pos[1], CARD_WIDTH_HOR, CARD_HEIGHT_HOR)




def create_chance_cards():
    cards = read_data.get_sheet('Chance')
    positions = get_cards_positions_horizontal()
    c = canvas.Canvas('cards/chance_cards.pdf', pagesize = reportlab.lib.pagesizes.A4)
    cnt = 0

    for card in cards:
        pos = positions[cnt]
        draw_chance_card_front(c, card, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    cnt = 0
    for i in range(len(cards)):
        pos = positions[cnt]
        draw_chance_card_back(c, pos)
        cnt += 1
        if cnt == 10:
            c.showPage()
            cnt = 0

    if cnt > 0:
        c.showPage()

    c.save()


def draw_chance_card_front(c, card, pos):

    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)
    c.rect(pos[0], pos[1], CARD_WIDTH_HOR, CARD_HEIGHT_HOR)

    padding = 0.3 * cm

    c.setStrokeColor(reportlab.lib.colors.black)
    c.setDash(3, 0)
    c.rect(pos[0] + padding, pos[1] + padding, CARD_WIDTH_HOR - 2 * padding, CARD_HEIGHT_HOR - 2 * padding)

    horizontal_middle = pos[0] + CARD_WIDTH_HOR / 2
    x_left = pos[0] + 2 * padding
    x_right = pos[0] + CARD_WIDTH_HOR - 2 * padding
    y = pos[1] + CARD_HEIGHT_HOR - padding - 0.8 * cm

    # c.setFillColor(reportlab.lib.colors.black)
    # c.setStrokeColor(reportlab.lib.colors.lightgrey)
    # c.setDash(2, 1)

    c.setFont("c-yaheibold", 15)
    c.drawCentredString(horizontal_middle, y, '机会  CHANCE')

    img_size = 2 * cm
    y -=  img_size + 0.5 * cm
    c.drawInlineImage(CHANCE, x_left + 0.7 * cm, y, width=img_size, height=img_size)

    c.setFont("c-yahei", 8)
    x_chinese = (x_left + img_size + 0.7 * cm + x_right) / 2

    if len(card['Chinese_3']) == 0:
        y += img_size - 1 * cm
    else:
        y += img_size - 0.5 * cm

    for i in range(3):
        title = 'Chinese_' + str(i+1)
        sentence = card[title].upper()
        c.drawCentredString(x_chinese, y, sentence)
        y -= 0.5 * cm

    if len(card['English_3']) == 0:
        y = pos[1] + CARD_HEIGHT_HOR - padding - 4.2 * cm
    else:
        y = pos[1] + CARD_HEIGHT_HOR - padding - 3.7 * cm

    x_english = (x_left + x_right) / 2

    for i in range(3):
        title = 'English_' + str(i+1)
        sentence = card[title].upper()
        c.drawCentredString(x_english, y, sentence)
        y -= 0.3 * cm

    y = pos[1] + CARD_HEIGHT_HOR - padding - 5 * cm
    c.setFont("c-yahei", 6)
    c.drawCentredString(x_english, y, '16 - ' + str(int(card['Index']) ))



def draw_chance_card_back(c, pos):
    c.setStrokeColor(reportlab.lib.colors.lightgrey)
    c.setDash(1, 3)

    c.drawInlineImage(CHANCE_BACK, pos[0], pos[1], width=CARD_WIDTH_HOR, height=CARD_HEIGHT_HOR)
    c.drawInlineImage(CHANCE, pos[0] + 0.5 * cm, pos[1] + 0.5 * cm, width=2 * cm, height=2 * cm)
    c.rect(pos[0], pos[1], CARD_WIDTH_HOR, CARD_HEIGHT_HOR)


if __name__ == '__main__':

    init()
    create_property_cards()
    create_service_cards()
    create_community_cards()
    create_chance_cards()




