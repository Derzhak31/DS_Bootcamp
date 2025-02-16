from config import num_of_steps, file_name, output_file, text
from analytics import Research

if __name__ == "__main__":
    res = Research(file_name)
    res_data = res.file_reader()
    res_calc = res.Calculations(res_data)
    h, t = res_calc.counts()
    pr_h, pr_t = res_calc.fractions(h, t)
    res_analytics = res.Analytics(res_data)
    ht_steps = res_analytics.predict_random(num_of_steps)
    h_steps, t_steps = res.Calculations(ht_steps).counts()
    context = text.format(h + t, h, t, pr_h, pr_t, num_of_steps, h_steps, t_steps)
    res_analytics.save_file(context, output_file)
