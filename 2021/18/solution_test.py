from solution import parse_input


def test_explode_1():
    tree = parse_input("[[[[[9,8],1],2],3],4]")
    tree.try_to_explode()
    assert str(tree) == "[[[[0,9],2],3],4]"


def test_explode_2():
    tree = parse_input("[7,[6,[5,[4,[3,2]]]]]")
    tree.try_to_explode()
    assert str(tree) == "[7,[6,[5,[7,0]]]]"


def test_explode_3():
    tree = parse_input("[[6,[5,[4,[3,2]]]],1]")
    tree.try_to_explode()
    assert str(tree) == "[[6,[5,[7,0]]],3]"


def test_explode_4():
    tree = parse_input("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    tree.try_to_explode()
    assert str(tree) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"


def test_explode_5():
    tree = parse_input("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    tree.try_to_explode()
    assert str(tree) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"


def test_reduce():
    tree_a = parse_input("[[[[4,3],4],4],[7,[[8,4],9]]]")
    tree_b = parse_input("[1,1]")
    sum = tree_a.add(tree_b)
    assert str(sum) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def test_magnitude():
    tree = parse_input("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
    assert 3488 == tree.magnitude()
