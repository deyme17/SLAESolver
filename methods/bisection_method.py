from methods.root_finder import RootFinder

class BisectionMethod(RootFinder):
    """Implementation of the bisection method"""
    
    def find_root(self, a, b):
        """
        Find root using bisection method.
        
        Args:
            a: Left boundary of interval
            b: Right boundary of interval
            
        Returns:
            Dictionary with results
        """
        self.history = []
        
        if not self.check_interval(a, b):
            raise ValueError(f"Function must have opposite signs at interval endpoints: f({a}) = {self.function(a)}, f({b}) = {self.function(b)}")
        
        iterations = 0
        
        while (b - a) > self.tolerance and iterations < self.max_iter:
            # mid
            c = (a + b) / 2
            
            self.history.append({
                'iter': iterations,
                'a': a,
                'b': b,
                'c': c,
                'fa': self.function(a),
                'fb': self.function(b),
                'fc': self.function(c),
                'interval': b - a
            })
            
            # check if we found the root
            if self.function(c) == 0:
                break
            
            # det which half to keep
            if self.function(c) * self.function(a) < 0:
                b = c
            else:
                a = c
            
            iterations += 1
        
        # final mid
        c = (a + b) / 2
        
        self.history.append({
            'iter': iterations,
            'a': a,
            'b': b,
            'c': c,
            'fa': self.function(a),
            'fb': self.function(b),
            'fc': self.function(c),
            'interval': b - a
        })
        
        return {
            'root': c,
            'iterations': iterations,
            'f_value': self.function(c),
            'tolerance': b - a,
            'history': self.history
        }