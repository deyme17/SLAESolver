from methods.root_finder import RootFinder

class ChordMethod(RootFinder):
    """Implementation of the chord method"""
    
    def find_root(self, a, b):
        """
        Find root using chord method.
        
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
        x_prev = a
        
        # init approximation
        x = a - (self.function(a) * (b - a)) / (self.function(b) - self.function(a))
        
        # tolerance check value
        delta = abs(x - x_prev)
        
        while delta > self.tolerance and iterations < self.max_iter:
            self.history.append({
                'iter': iterations,
                'a': a,
                'b': b,
                'x': x,
                'fa': self.function(a),
                'fb': self.function(b),
                'fx': self.function(x),
                'delta': delta
            })
            
            # check if we found the root
            if self.function(x) == 0:
                break
            
            # update interval
            if self.function(x) * self.function(a) < 0:
                b = x
            else:
                a = x
            
            x_prev = x
            x = a - (self.function(a) * (b - a)) / (self.function(b) - self.function(a))
            
            delta = abs(x - x_prev)
            
            iterations += 1

        self.history.append({
            'iter': iterations,
            'a': a,
            'b': b,
            'x': x,
            'fa': self.function(a),
            'fb': self.function(b),
            'fx': self.function(x),
            'delta': delta
        })
        
        return {
            'root': x,
            'iterations': iterations,
            'f_value': self.function(x),
            'tolerance': delta,
            'history': self.history
        }