import json
import sys

def calculate_metrics(resources, noise):
    # Аксиома 1: Литеральный расчет Ресурсов D = sum(r * w)
    d_total = sum(r['volume'] * r['weight'] for r in resources)
    
    # Аксиома 2: Математическое определение Кредита Доверия C_trust = D / E_noise
    e_noise = max(noise, 0.0001)
    c_trust = d_total / e_noise
    
    # Аксиома 3: Ответственность Нейропротокола на основе верифицированных фактов
    facts_count = len([r for r in resources if r['verified']])
    r_neuro = c_trust * facts_count
    
    return {
        "volume_d_total": round(d_total, 4),
        "credit_c_trust": round(c_trust, 4),
        "responsibility_r_neuro": round(r_neuro, 4)
    }

def main():
    try:
        with open('manifest.json', 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
        
    # Входной поток данных из сокетов (Тестовый слепок фактов)
    sample_resources = [
        {"volume": 150, "weight": 1.0, "verified": True},
        {"volume": 50, "weight": 0.9, "verified": True},
        {"volume": 200, "weight": 0.1, "verified": False}
    ]
    current_noise = 0.02  # Уровень фонового шума среды (2%)
    
    metrics = calculate_metrics(sample_resources, current_noise)
    
    output = {
        "node": manifest.get("node_type", "Core"),
        "engine": manifest["mathematical_engine"]["module"],
        "status": "Уровень беспристрастности и фактической ясности",
        "metrics": metrics
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
