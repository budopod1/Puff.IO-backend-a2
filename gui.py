from tiles import Leaves, Flowers, Grass, Trader1, Stone, Wood
from utils import pad_list
from tiles import Tile, Empty, Arrow, tile_names, tile_order
from shortsocket import Array


all_trades = {
    1: [
        (((Leaves, 1), (Grass, 2)), (Flowers, 1)),
        (((Trader1, 2),), (Stone, 5)),
        (((Wood, 5),), (Leaves, 1))
    ]
}


def inventory_gui(player):
    items = sorted(
        player.inventory,
        key=lambda k: tile_order.inverse[tile_names.inverse[k]]
    )
    amounts = [player.inventory[item] for item in items]
    return make_gui(
        [
            tile_names.inverse[item]
            for item in items
        ],
        amounts,
        8, 4
    )

def trader1_gui(player):
    trades = all_trades[1]
    return make_gui(
        *zip(*[
            item
            for trade in [
                [
                    *pad_list(take, 2, (Empty(), 1)),
                    (Arrow(), 1),
                    give,
                    *([(Empty(), 1)] if i % 2 == 0 else [])
                ]
                for i, (take, give) in enumerate(trades)
            ]
            for item in trade
        ]), 9, 5, Empty
    )

def make_gui(items, amounts, width, height, otherwise=Tile,
             slots=None):
    items = list(items[::-1])
    amounts = list(amounts[::-1])
    return Array([
        Array([
            (items.pop().TYPE if items else otherwise.TYPE)
            if slots is None or (x, y) in slots else 
            otherwise.TYPE
            for x in range(width)
            for y in range(height)
        ], dtype="int8"),
        Array([
            (amounts.pop() if amounts else 1)
            if slots is None or (x, y) in slots else
            1
            for x in range(width)
            for y in range(height)
        ], dtype="int8")
    ])


guis = {
    1: inventory_gui,
    2: trader1_gui
}
