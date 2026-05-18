# Changelog 📃

## V1.2.0 - 2026-05-18
### Added
- Graphic method strategy
- Graphic method view for 2 varaibles problem (with 2D plane)
- A selector method for graphic method and simplex (big M) strategies, the first one is diseabled when more than 2 vars are used

### Fixed
- An error ocurred when putting double values for the constraints or the objetcive function.

### Refactored
- System optimized: Removing additional methods callings, and optimizated components comunication

## V1.1.0 - 2026-05-11
### Added
- New result view, visualice the last table iteration, the objective function value and the non-zero varaibles values
### Fixed
- Repeated rows building the tableau

### Refactored
- Added a QStackedWidget for working differents views in a single MainWindow

## V1.0.0 - 2026-05-06
First version of the software