# src/game_logic.py
import random

class QuestionGenerator:
    def __init__(self):
        self.fruits = ["apel", "jeruk"]

    def generate(self, difficulty, level):
        """
        Membuat soal matematika random.
        """
        # --- Tentukan Operator ---
        if difficulty == "easy":
            ops = ["+", "-"]
        elif difficulty == "medium":
            ops = ["x", ":"]
        else: # hard
            ops = ["+", "-", "x", ":"]
            
        operator = random.choice(ops)
        
        num_a = 0
        num_b = 0
        ans = 0
        
        # --- Logika Angka (Disesuaikan agar visual buah tidak terlalu penuh) ---
        # Kita batasi jumlah buah agar muat di layar (max sekitar 20-25 per grup)
        
        if operator == "+":
            # Level 1: 1-5, Level 10: 10-20
            limit = 2 + (level * 2) 
            num_a = random.randint(1, limit)
            num_b = random.randint(1, limit)
            ans = num_a + num_b
            
        elif operator == "-":
            limit = 3 + (level * 2)
            num_a = random.randint(2, limit + 2)
            num_b = random.randint(1, num_a) # Pengurang tidak boleh lebih besar
            ans = num_a - num_b
            
        elif operator == "x":
            # Perkalian angka kecil (misal 2x3, 4x5) agar visualisasi masuk akal
            limit_a = 1 + int(level / 2.5) 
            limit_b = 1 + int(level / 2)
            num_a = random.randint(1, max(2, limit_a))
            num_b = random.randint(1, max(2, limit_b))
            ans = num_a * num_b
            
        elif operator == ":":
            # Pembagian: Tentukan hasil dulu biar bulat
            divisor = random.randint(2, 3 + int(level/3))
            quotient = random.randint(1, 2 + int(level/2))
            num_b = divisor
            ans = quotient
            num_a = divisor * quotient # Total buah

        # --- Pilihan Ganda ---
        choices = {ans}
        while len(choices) < 4:
            fake = ans + random.randint(-5, 5)
            if fake >= 0 and fake != ans:
                choices.add(fake)
        
        choices_list = list(choices)
        random.shuffle(choices_list)

        return {
            "a": num_a,
            "b": num_b,
            "op": operator,
            "ans": ans,
            "choices": choices_list,
            "fruit": random.choice(self.fruits)
        }