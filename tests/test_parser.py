from textwrap import dedent
from iter_tokens import iter_tokens


def test_iter_tokens(capsys):
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)
    assert capsys.readouterr().out == dedent(
        """\
TokenNum(2.0)
Token(PLUS)
Token(LPAREN)
TokenNum(3.0)
Token(MUL)
TokenNum(4.0)
Token(RPAREN)
Token(PLUS)
TokenNum(5.0)
        """
    )
