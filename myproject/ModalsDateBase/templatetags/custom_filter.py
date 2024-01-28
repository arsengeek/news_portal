from django import template

register = template.Library()

WORDS_MAT = ['fuck', 'beatch', 'Fuck', 'Beatch','shit','Shit', 'Nigga', 'nigga']

@register.filter(name='currency')
def currency(value):
    words = value.split()
    for i in range(len(words)):
        for word_mat in WORDS_MAT:
            if words[i] == word_mat:
                words[i] = words[i][0] + '*' * (len(words[i]) - 1)
    value = ' '.join(words)
    return value