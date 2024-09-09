# Prioridades de los operadores
precedence = {'+': 1, '.': 2, '*': 3}

# Función para verificar si un carácter es un operador
def is_operator(c: str) -> bool:
    return c in precedence

# Función para verificar si un carácter es un operando
def is_operand(c: str) -> bool:
    return c.isalnum() or c == '_'

# Función para insertar puntos de concatenación en la expresión infija
def insert_concatenation_operators(infix: str) -> str:
    result = []
    length = len(infix)

    for i in range(length):
        result.append(infix[i])
        if i < length - 1:
            if (is_operand(infix[i]) and (is_operand(infix[i+1]) or infix[i+1] == '(')) or \
               (infix[i] == ')' and (is_operand(infix[i+1]) or infix[i+1] == '(')) or \
               (infix[i] == '*' and (is_operand(infix[i+1]) or infix[i+1] == '(')):
                result.append('.')

    return ''.join(result)

# Función principal para convertir una expresión infija a postfija
def toPostFix(infixExpression: str) -> str:
    # Primero, inserta los puntos de concatenación explícitos
    infixExpression = insert_concatenation_operators(infixExpression)

    output = []
    operators = []

    i = 0
    while i < len(infixExpression):
        c = infixExpression[i]

        if is_operand(c):  # Si es un operando, añadirlo a la salida
            output.append(c)
        elif c == '(':  # Si es un paréntesis abierto, apilarlo
            operators.append(c)
        elif c == ')':  # Si es un paréntesis cerrado, desapilar hasta el paréntesis abierto
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Eliminar el paréntesis abierto
        elif is_operator(c):  # Si es un operador
            while (operators and operators[-1] != '(' and
                   precedence[operators[-1]] >= precedence[c]):
                output.append(operators.pop())
            operators.append(c)
        i += 1

    # Desapilar cualquier operador restante
    while operators:
        output.append(operators.pop())

    return ''.join(output)

# Ejemplo de uso
if __name__ == "__main__":
    infix = "(0+1)*11(0+1)*"
    postfix = toPostFix(infix)
    print(f"Infijo: {infix}")
    print(f"Postfijo: {postfix}")