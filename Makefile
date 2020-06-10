.DEFAULT_GOAL := help
.PHONY : clean help ALL

SQLIZED_DB = data/wrapped/sqlized.sqlite

COMPILED_AGENCIES = data/compiled/state-agencies.csv
WRANGLED_AGENCIES = data/wrangled/state-agencies.csv

help:
	@echo 'Run `make ALL` to see how things run from scratch'

ALL: clean sqlize


clean: clean_sqlize
	@echo --- Cleaning stubs
	rm -f $(STUB_WRANGLED)
	rm -f $(STUB_FUSED)
	rm -f $(STUB_COLLECTED)


clean_sqlize:
	test -f $(SQLIZED_DB)  && rm $(SQLIZED_DB) || true

# change sqlize task to do something else besides sqlize_bootstrap.sh,
# when you need something more sophisticated
sqlize: $(SQLIZED_DB)
# create data/sqlized/mydata.sqlite from CSVs in wrangled
$(SQLIZED_DB): wrangle clean_sqlize
	@echo ""
	@echo --- SQLizing tables $@
	@echo
	./scripts/sqlize.sh \
      $(SQLIZED_DB) data/compiled compiled

	@echo ""
	@echo "---"
	./scripts/sqlize.sh \
      $(SQLIZED_DB) data/wrangled wrangled


	@echo ""
	@echo ""
	@echo ""
	@echo "--- Open database with this command:"
	@echo ""
	@echo "      " open $(SQLIZED_DB)


wrangle: $(WRANGLED_AGENCIES)

$(WRANGLED_AGENCIES): $(COMPILED_AGENCIES)
	./scripts/wrangle.py > $(WRANGLED_AGENCIES)


compile: $(COMPILED_AGENCIES)

$(COMPILED_AGENCIES):
	@echo "Compiling to $(COMPILED_AGENCIES)"
	./scripts/compile/compile_state_agencies.py > $(COMPILED_AGENCIES)

convert: data/collected/disp/agencies/
	./scripts/collect/collect_convert_csvs.py


collect:
	@echo "Gathers $(STUB_COLLECTED)"
	./scripts/collect/collect_spreadsheets.py
