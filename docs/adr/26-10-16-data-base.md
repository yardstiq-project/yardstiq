# Yarstiq Data Base

**Context:** Yardtisq need to allow module and algo import but avoid duplicating data made by qall
**Decision:** Yardstiq's db only stores qall hash with metadata
**Reasons:** Importing a module/algo pushs it on qall registry meaning no need to store anything but the hash to recover it later