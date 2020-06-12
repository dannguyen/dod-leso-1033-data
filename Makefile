.DEFAULT_GOAL := help
.PHONY : clean help ALL


#COMPILED_AGENCIES = data/compiled/state-agencies/ALL.csv
WRANGLED_AGENCIES = data/wrangled/state-agencies.csv

help:
	@echo 'look at makefile TKTK'

ALL: clean

clean:
	@echo --- Cleaning


# clean: clean_sqlize
# 	@echo --- Cleaning stubs
# 	rm -f $(STUB_WRANGLED)
# 	rm -f $(STUB_FUSED)
# 	rm -f $(STUB_COLLECTED)

sqlize_compile:
	scripts/wrap/sqlize/tablemaker.py \
	    --db data/wrapped/db.sqlite \
	    --src data/compiled/state-agencies/ALL.csv \
	    --table 'compiled_agency' \
	    --create scripts/wrap/sqlize/schemas/tbl_compiled_agency.sql \
	    --index scripts/wrap/sqlize/schemas/idx_compiled_agency.sql \
	    --drop



# wrangle: $(WRANGLED_AGENCIES)

# $(WRANGLED_AGENCIES): $(COMPILED_AGENCIES)
# 	./scripts/wrangle.py > $(WRANGLED_AGENCIES)



compile:
	@echo "Compiling..."
	./scripts/compile/compile_state_agencies.py


# compile: $(COMPILED_AGENCIES)

# $(COMPILED_AGENCIES):
# 	@echo "Compiling to $(COMPILED_AGENCIES)"
# 	./scripts/compile/compile_state_agencies.py > $(COMPILED_AGENCIES)

convert: data/collected/disp/agencies/
	./scripts/collect/collect_convert_csvs.py


collect:
	@echo "Gathers $(STUB_COLLECTED)"
	./scripts/collect/collect_spreadsheets.py
