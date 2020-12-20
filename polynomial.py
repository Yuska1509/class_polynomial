class Polynomial:
    def __init__(self, *coefficients):
        poly_dict = {}
        j = 0
        for elem in coefficients:
            if isinstance(elem, list):
                for i in range(len(elem)):
                    poly_dict[i] = int(elem[i])
            elif isinstance(elem, dict):
                for key in sorted(elem.keys()):
                    poly_dict[int(key)] = int(elem[key])
            elif isinstance(elem, int):
                poly_dict[j] = elem
                j += 1
            elif isinstance(elem, Polynomial):
                poly_dict = elem.dict
        coeff_list = [poly_dict.get(i, 0) for i
                      in range(max((poly_dict.keys())) + 1)]
        n = len(coeff_list) - 1
        while coeff_list[n] == 0 and n > 0:
            coeff_list.pop(n)
            poly_dict.pop(n, 0)
            n -= 1
        for i in range(len(coeff_list)):
            if coeff_list[i] == 0:
                poly_dict.pop(i, 0)
        if poly_dict == {}:
            poly_dict[0] = 0
        self.dict = poly_dict
        self.coeff = coeff_list

    def __repr__(self):
        return 'Polynomial ' + str(self.coeff)

    def __str__(self):
        answer = ''
        for i in range(len(self.coeff) - 1, - 1, - 1):
            coef = self.coeff[i]
            if i == len(self.coeff) - 1 and coef < 0:
                answer += '-'
            elif i != len(self.coeff) - 1:
                if coef > 0:
                    answer += ' + '
                elif coef < 0:
                    answer += ' - '
            if coef != 0:
                if (coef != 1 and coef != -1) or i == 0:
                    answer += str(abs(coef))
                if i != 0:
                    answer += 'x'
                    if i != 1 and i != 0:
                        answer += '^'
                        answer += str(i)
            if len(self.coeff) - 1 == 0 and coef == 0:
                answer += '0'
        return answer

    def __eq__(self, other):
        other = Polynomial(other)
        return self.coeff == other.coeff

    def __add__(self, other):
        other = Polynomial(other)
        new_dict = {i: self.dict.get(i, 0) + other.dict.get(i, 0)
                    for i in range(max(self.degree(), other.degree()) + 1)}
        return Polynomial(new_dict)

    def __radd__(self, other):
        return self + Polynomial(other)

    def __neg__(self):
        return Polynomial([- elem for elem in self.coeff])

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (- self)

    def __call__(self, x):
        answer = 0
        for key in self.dict.keys():
            answer += self.dict[key] * x ** key
        return answer

    def degree(self):
        return max(self.dict.keys())

    def der_1(self):
        new_dict = self.dict.copy()
        for key in self.dict.keys():
            if key != 0:
                new_dict.update({key - 1: key * new_dict[key]})
        new_dict.pop(max(new_dict.keys()))
        return Polynomial(new_dict)

    def der(self, d=1):
        if self.degree() < d:
            return '0'
        else:
            answer_dict = Polynomial(self.dict)
            for i in range(d):
                answer_dict = Polynomial(answer_dict.der_1())
            return answer_dict

    def __mul__(self, other):
        other = Polynomial(other)
        new_dict = {}
        for key1 in self.dict.keys():
            for key2 in other.dict.keys():
                new_dict.update({key1 + key2: new_dict.get(key1 + key2, 0)
                                      + self.dict[key1] * other.dict[key2]})
        return Polynomial(new_dict)

    def __rmul__(self, other):
        return self * other

    def __iter__(self):
        self.max = len(self.dict.keys())
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            result = list(self.dict.keys())[self.n], \
                     self.dict[list(self.dict.keys())[self.n]]
            self.n += 1
            return result
        else:
            raise StopIteration


class NotOddDegreeException(BaseException):
    pass


class DegreeIsTooBigException(BaseException):
    pass


class RealPolynomial(Polynomial):
    def __init__(self, *coefficients):
        poly_dict = {}
        j = 0
        for elem in coefficients:
            if isinstance(elem, list):
                for i in range(len(elem)):
                    poly_dict[i] = float(elem[i])
            elif isinstance(elem, dict):
                for key in sorted(elem.keys()):
                    poly_dict[int(key)] = float(elem[key])
            elif isinstance(elem, int) or isinstance(elem, float):
                poly_dict[j] = elem
                j += 1
            elif isinstance(elem, Polynomial):
                poly_dict = elem.dict
        coeff_list = [poly_dict.get(i, 0)
                      for i in range(max((poly_dict.keys())) + 1)]
        n = len(coeff_list) - 1
        while coeff_list[n] == 0 and n > 0:
            coeff_list.pop(n)
            poly_dict.pop(n, 0)
            n -= 1
        for i in range(len(coeff_list)):
            if coeff_list[i] == 0:
                poly_dict.pop(i, 0)
        if poly_dict == {}:
            poly_dict[0] = 0
        self.dict = poly_dict
        self.coeff = coeff_list
        if self.degree() % 2 != 1:
            raise NotOddDegreeException

    def find_root(self):
        a = -10000
        b = a
        eps = 1e-6
        if self(a) == 0:
            return a
        if self(a) < 0:
            while self(b) < 0 and b < 10000:
                b += 1000
        if self(a) > 0:
            while self(b) > 0 and b < 10000:
                b += 1000
        while abs(self(a)) > eps:
            x = (a + b) / 2
            if self(a) < 0 and self(x) <= 0 or \
                    self(a) > 0 and self(x) >= 0:
                a = x
            else:
                b = x
        a = b
        return a


class QuadraticPolynomial(Polynomial):
    def __init__(self, *coefficients):
        poly_dict = {}
        j = 0
        for elem in coefficients:
            if isinstance(elem, list):
                for i in range(len(elem)):
                    poly_dict[i] = int(elem[i])
            elif isinstance(elem, dict):
                for key in sorted(elem.keys()):
                    poly_dict[int(key)] = int(elem[key])
            elif isinstance(elem, int):
                poly_dict[j] = elem
                j += 1
            elif isinstance(elem, Polynomial):
                poly_dict = elem.dict
        coeff_list = [poly_dict.get(i, 0)
                      for i in range(max((poly_dict.keys())) + 1)]
        n = len(coeff_list) - 1
        while coeff_list[n] == 0 and n > 0:
            coeff_list.pop(n)
            poly_dict.pop(n, 0)
            n -= 1
        for i in range(len(coeff_list)):
            if coeff_list[i] == 0:
                poly_dict.pop(i, 0)
        if poly_dict == {}:
            poly_dict[0] = 0
        self.dict = poly_dict
        self.coeff = coeff_list
        if self.degree() > 2:
            raise DegreeIsTooBigException

    def solve(self):
        a = self.dict.get(2, 0)
        b = self.dict.get(1, 0)
        c = self.dict.get(0, 0)
        if a != 0:
            D = b ** 2 - 4 * a * c
            if D > 0:
                answer = [(- b + D ** (1 / 2)) / (2 * a),
                          (- b - D ** (1 / 2)) / (2 * a)]
            elif D == 0:
                answer = [- b / 2 * a]
            else:
                answer = []
        elif a == 0 and b != 0:
            answer = [- c / b]
        else:
            answer = []
        return answer


p1 = Polynomial(1, 0, 0, 0)
p2 = Polynomial([2, 0, -1, 1])
p3 = Polynomial({2: 1, 5: 1})
p4 = Polynomial({3: -2, 0: 3})
for i in p4:
    print(i)
print(-2 + p4 + 1 + p3 - 2)
p5 = RealPolynomial({3: 2})
print(p5)