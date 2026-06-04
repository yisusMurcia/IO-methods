# Changelog 📃

## V 1.3.3 - 2026-06-04
Fixed:
- Empty window when use the back button
    - Deleting wrong view when using this function
- Sensitivility analizer doesn´t working in big M method
    - The inverse matrix has the artificial variables, causing an imposible matrix multiplication, the sizes didn´t match.
    - Using the varname as a index position

## V1.3.2 - 2026-05-21
### Added
A clean all button to restore the entry problem view for a new problem

## V1.3.1 - 2026-05-20

### Added
A back button for results views

## V1.3.0 - 2026-05-20
### Added
Sensibility analysis for graphical method

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