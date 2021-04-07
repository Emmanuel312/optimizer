# Generated from antlr4-python3-runtime-4.7.2/src/autogen/Grammar.g4 by ANTLR 4.7.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser


# retorne Type.INT, etc para fazer checagem de tipos
class Type:
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    STRING = "char *"


# This class defines a complete generic visitor for a parse tree produced by GrammarParser.
class GrammarCheckerVisitor(ParseTreeVisitor):
    ids_defined = {}  # armazenar informações necessárias para cada identifier definido
    inside_what_function = ""

    # Visit a parse tree produced by GrammarParser#fiile.
    def visitFiile(self, ctx: GrammarParser.FiileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#function_definition.
    def visitFunction_definition(self, ctx: GrammarParser.Function_definitionContext):
        tyype = ctx.tyype().getText()
        name = ctx.identifier().getText()
        params = self.visit(ctx.arguments())
        self.ids_defined[name] = tyype, params, None
        self.inside_what_function = name
        self.visit(ctx.body())
        return

    # Visit a parse tree produced by GrammarParser#body.
    def visitBody(self, ctx: GrammarParser.BodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#statement.
    def visitStatement(self, ctx: GrammarParser.StatementContext):
        if ctx.RETURN() != None:
            token = ctx.RETURN().getPayload()
            tyype, _ = self.visit(ctx.expression())
            function_type, params, _ = self.ids_defined[self.inside_what_function]
            if function_type == Type.INT and tyype == Type.FLOAT:
                print(
                    "WARNING: possible loss of information returning float expression from int function '" + self.inside_what_function + "' in line " + str(
                        token.line) + " and column " + str(token.column))
            elif function_type == Type.VOID and tyype != Type.VOID:
                print(
                    "ERROR: trying to return a non void expression from void function '" + self.inside_what_function + "' in line " + str(
                        token.line) + " and column " + str(token.column))
            elif function_type != Type.VOID and tyype == Type.VOID:
                print(
                    "ERROR: trying to return void expression from function '" + self.inside_what_function + "' in line " + str(
                        token.line) + " and column " + str(token.column))

        else:
            self.visitChildren(ctx)
        return

    # Visit a parse tree produced by GrammarParser#if_statement.
    def visitIf_statement(self, ctx: GrammarParser.If_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#else_statement.
    def visitElse_statement(self, ctx: GrammarParser.Else_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_loop.
    def visitFor_loop(self, ctx: GrammarParser.For_loopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_initializer.
    def visitFor_initializer(self, ctx: GrammarParser.For_initializerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_condition.
    def visitFor_condition(self, ctx: GrammarParser.For_conditionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_step.
    def visitFor_step(self, ctx: GrammarParser.For_stepContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#variable_definition.
    def visitVariable_definition(self, ctx: GrammarParser.Variable_definitionContext):
        tyype = ctx.tyype().getText()

        for i in range(len(ctx.identifier())):
            name = ctx.identifier(i).getText()
            token = ctx.identifier(i).IDENTIFIER().getPayload()
            if ctx.expression(i) != None:
                # print(ctx.expression(i).getText())
                expr_type, const_value = self.visit(ctx.expression(i))
                if expr_type == Type.VOID or expr_type == Type.STRING:
                    print(
                        "ERROR: trying to assign '" + expr_type + "' expression to variable '" + name + "' in line " + str(
                            token.line) + " and column " + str(token.column))
                elif expr_type == Type.FLOAT and tyype == Type.INT:
                    print(
                        "WARNING: possible loss of information assigning float expression to int variable '" + name + "' in line " + str(
                            token.line) + " and column " + str(token.column))
                # print("noExpr")
            else:
                const_value = None
            self.ids_defined[
                name] = tyype, -1, const_value  # -1 means not a array, therefore no length here (vide 15 lines below)

        for i in range(len(ctx.array())):
            name = ctx.array(i).identifier().getText()
            token = ctx.array(i).identifier().IDENTIFIER().getPayload()
            if ctx.array_literal(i) != None:
                expr_types, const_array_values = self.visit(ctx.array_literal(i))
                for j in range(len(expr_types)):
                    if expr_types[j] == Type.VOID or expr_types[j] == Type.STRING:
                        print("ERROR: trying to initialize '" + expr_types[
                            j] + "' expression to '" + tyype + "' array '" + name + "' at index " + str(
                            j) + " of array literal in line " + str(token.line) + " and column " + str(token.column))
                    elif expr_types[j] == Type.FLOAT and tyype == Type.INT:
                        print(
                            "WARNING: possible loss of information initializing float expression to int array '" + name + "' at index " + str(
                                j) + " of array literal in line " + str(token.line) + " and column " + str(
                                token.column))
            else:
                const_array_values = None
            array_length = self.visit(ctx.array(i))
            self.ids_defined[name] = tyype, array_length, const_array_values

        return

    # Visit a parse tree produced by GrammarParser#variable_assignment.
    def visitVariable_assignment(self, ctx: GrammarParser.Variable_assignmentContext):
        op = ctx.OP.text
        if ctx.identifier() != None:
            name = ctx.identifier().getText()
            token = ctx.identifier().IDENTIFIER().getPayload()
            try:
                tyype, _, const_value = self.ids_defined[name]
            except:
                print("ERROR: undefined variable '" + name + "' in line " + str(token.line) + " and column " + str(
                    token.column))
                return

        else:
            name = ctx.array().identifier().getText()
            token = ctx.array().identifier().IDENTIFIER().getPayload()
            try:
                tyype, array_length, const_array_values = self.ids_defined[name]
            except:
                print("ERROR: undefined array '" + name + "' in line " + str(token.line) + " and column " + str(
                    token.column))
            # return array index
            index = self.visit(ctx.array())
            if const_array_values:
                const_value = const_array_values[index]
            else:
                const_value = None

        op = ctx.OP.text
        if op in ['++', '--']:
            if not const_value:
                const_value = None
            else:
                const_value = eval(f"const_value {op[0]} 1")
        else:
            expr_type, expr_const_value = self.visit(ctx.expression())
            if expr_type == Type.VOID or expr_type == Type.STRING:
                print(
                    "ERROR: trying to assign '" + expr_type + "' expression to variable '" + name + "' in line " + str(
                        token.line) + " and column " + str(token.column))
            elif expr_type == Type.FLOAT and tyype == Type.INT:
                print(
                    "WARNING: possible loss of information assigning float expression to int variable '" + name + "' in line " + str(
                        token.line) + " and column " + str(token.column))
            if op == '=':
                const_value = expr_const_value
            elif not (expr_const_value and const_value):
                const_value = None
            # compound operators
            elif op in ['+=', '-=', '*=', '/=']:
                const_value = eval(f"const_value {op[0]} expr_const_value")
            # commons operators
            else:
                const_value = eval(f"const_value {op} expr_const_value")

        if ctx.identifier() != None:
            self.ids_defined[name] = tyype, -1, const_value
        else:  # array
            if const_array_values:
                const_array_values[index] = const_value
            self.ids_defined[name] = tyype, array_length, const_array_values
        return

    # Visit a parse tree produced by GrammarParser#expression.
    def visitExpression(self, ctx: GrammarParser.ExpressionContext):
        tyype = Type.VOID
        const_value = None
        if len(ctx.expression()) == 0:

            if ctx.integer():
                tyype = Type.INT
                # forced a cast type
                const_value = int(ctx.integer().getText())

            elif ctx.floating():
                tyype = Type.FLOAT
                const_value = float(ctx.floating().getText())

            elif ctx.string():
                tyype = Type.STRING
                const_value = str(ctx.string().getText())

            elif ctx.identifier():
                name = ctx.identifier().getText()
                try:
                    tyype, _, const_value = self.ids_defined[name]
                except:
                    token = ctx.identifier().IDENTIFIER().getPayload()
                    print("ERROR: undefined variable '" + name + "' in line " + str(token.line) + " and column " + str(
                        token.column))

            elif ctx.array():
                name = ctx.array().identifier().getText()
                try:
                    tyype, array_length, const_array_values = self.ids_defined[name]
                except:
                    token = ctx.array().identifier().IDENTIFIER().getPayload()
                    print("ERROR: undefined array '" + name + "' in line " + str(token.line) + " and column " + str(
                        token.column))
                array_index = self.visit(ctx.array())
                if array_index and array_length:
                    if array_index < 0 or array_index >= array_length:
                        token = ctx.array().identifier().IDENTIFIER().getPayload()
                        print("ERROR:  array '" + name + "' index out of bounds in line " + str(
                            token.line) + " and column " + str(token.column))
                    elif const_array_values:
                        const_value = const_array_values[array_index]

            elif ctx.function_call() != None:
                tyype, const_value = self.visit(ctx.function_call())

        elif len(ctx.expression()) == 1:

            if ctx.OP != None:  # unary operators
                text = ctx.OP.text
                token = ctx.OP
                tyype, const_value = self.visit(ctx.expression(0))
                const_value = eval(f"{text} const_value")
                if tyype == Type.VOID:
                    print("ERROR: unary operator '" + text + "' used on type void in line " + str(
                        token.line) + " and column " + str(token.column))

            else:  # parentheses
                tyype, const_value = self.visit(ctx.expression(0))

        elif len(ctx.expression()) == 2:  # binary operators
            text = ctx.OP.text
            token = ctx.OP
            left, left_const_value = self.visit(ctx.expression(0))
            right, right_const_value = self.visit(ctx.expression(1))
            if left == Type.VOID or right == Type.VOID:
                print("ERROR: binary operator '" + text + "' used on type void in line " + str(
                    token.line) + " and column " + str(token.column))

            if text == '*' or text == '/' or text == '+' or text == '-':
                if left == Type.FLOAT or right == Type.FLOAT:
                    tyype = Type.FLOAT
                else:
                    tyype = Type.INT
            else:
                tyype = Type.INT
            # check if both values is not None and check if both is not string
            if left_const_value and right_const_value and Type.STRING not in [left, right]:
                const_value = eval(f"left_const_value {text} right_const_value")
                # if const_value is a boolean just convert it to int
                if isinstance(const_value, bool):
                    const_value = int(const_value)
                print(
                    f"line {token.line} Expression {left_const_value} {text} {right_const_value} "
                    f"simplified to: {const_value}")

        return tyype, const_value

    # Visit a parse tree produced by GrammarParser#array.
    def visitArray(self, ctx: GrammarParser.ArrayContext):
        tyype, const_value = self.visit(ctx.expression())
        if tyype != Type.INT:
            token = ctx.identifier().IDENTIFIER().getPayload()
            print("ERROR: array expression must be an integer, but it is " + str(tyype) + " in line " + str(
                token.line) + " and column " + str(token.column))
        return const_value

    # Visit a parse tree produced by GrammarParser#array_literal.
    def visitArray_literal(self, ctx: GrammarParser.Array_literalContext):
        types = []
        const_values_array = []
        for i in range(len(ctx.expression())):
            tyype, const_value = self.visit(ctx.expression(i))
            types += [tyype]
            const_values_array.append(const_value)
        return types, const_values_array

    # Visit a parse tree produced by GrammarParser#function_call.
    def visitFunction_call(self, ctx: GrammarParser.Function_callContext):
        name = ctx.identifier().getText()
        token = ctx.identifier().IDENTIFIER().getPayload()
        try:
            tyype, args, const_value = self.ids_defined[name]
            if len(args) != len(ctx.expression()):
                # for i in range(len(ctx.expression())):
                #    print(ctx.expression(i).getText())
                print("ERROR: incorrect number of parameters for function '" + name + "' in line " + str(
                    token.line) + " and column " + str(token.column) + ". Expecting " + str(len(args)) + ", but " + str(
                    len(ctx.expression())) + " were given")
        except:
            print("ERROR: undefined function '" + name + "' in line " + str(token.line) + " and column " + str(
                token.column))

        for i in range(len(ctx.expression())):
            arg_type, _ = self.visit(ctx.expression(i))
            if i < len(args):
                if arg_type == Type.VOID:
                    print("ERROR: void expression passed as parameter " + str(
                        i) + " of function '" + name + "' in line " + str(token.line) + " and column " + str(
                        token.column))
                elif arg_type == Type.FLOAT and args[i] == Type.INT:
                    print(
                        "WARNING: possible loss of information converting float expression to int expression in parameter " + str(
                            i) + " of function '" + name + "' in line " + str(token.line) + " and column " + str(
                            token.column))
        return tyype, const_value

    # Visit a parse tree produced by GrammarParser#arguments.
    def visitArguments(self, ctx: GrammarParser.ArgumentsContext):
        params = []
        for i in range(len(ctx.identifier())):
            tyype = ctx.tyype(i).getText()
            name = ctx.identifier(i).getText()
            self.ids_defined[name] = tyype, -1, None
            params += [tyype]
        return params

    # Visit a parse tree produced by GrammarParser#tyype.
    def visitTyype(self, ctx: GrammarParser.TyypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#integer.
    def visitInteger(self, ctx: GrammarParser.IntegerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#floating.
    def visitFloating(self, ctx: GrammarParser.FloatingContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#string.
    def visitString(self, ctx: GrammarParser.StringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#identifier.
    def visitIdentifier(self, ctx: GrammarParser.IdentifierContext):
        return self.visitChildren(ctx)

    # del GrammarParser

    # def aggregateResult(self, aggregate:Type, next_result:Type):
    # return next_result if next_result != None else aggregate
