import sys

def draw_separator(n):
    """
    Draws separator used between texts

    :param n: Number of # symbols that should be used to draw the separator
    :type n: int
    :return: Prints separator in format - ########
    """
    try:
        print("#" * n)
    except ValueError:
        sys.exit("draw_separator's parameter n should be an integer")


def center_text(text, length, draw_border=False, double_border=False):
    """
    Centers text on a specified character length

    :param text: Text to be centered
    :type text: str
    :param length: Length of the whole output
    :type length: int
    :param draw_border: Draws '#' at the begging and end of a line
    :type draw_border:bool
    :return Prints centered text
    """
    try:
        if draw_border:
            if double_border:
                print("##", text.center(length - 4), "##", sep="")
            else:
                print("#", text.center(length - 2), "#", sep="")
        else:
            print(text.center(length))
    except ValueError:
        sys("center_text's text must be a string and length an integer")
