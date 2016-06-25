full_results_ideal_settings.txt: output from convert.py
parseandplot_full_dataset.py: script that parses raw data and generates graphs (put directly into figures directory)
full_parsed_results_ideal_settings.txt: parsed output 

command called:
python parseandplot_full_dataset.py full_results_ideal_settings.txt IdealSettings > full_parsed_results_ideal_settings.txt
python parseandplot_full_dataset.py full_results_default_settings.txt DefaultSettings > full_parsed_results_default_settings.txt

Figures output to: 
../../figures/
