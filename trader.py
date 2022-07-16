from tiles import Leaves, Flowers, Grass, Trader1, Stone, Wood


all_trades = {
    1: [
        (((Leaves, 1), (Grass, 2)), (Flowers, 1)),
        (((Trader1, 2),), (Stone, 5)),
        (((Wood, 5),), (Leaves, 1))
    ]
}
