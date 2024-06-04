from concordance_machine import ConcordanceMachine

# TODO: Add config file with run parameters

cm = ConcordanceMachine(books=['Romans', 'James'])

cm.get_html_files()
print(cm.html_files)

cm.read_html_files()

print(cm.verses)

cm.generate_concordance()

print(cm.concordance)

# Add user input for generating export files

cm.export_concordance(concordance_type="phrase")