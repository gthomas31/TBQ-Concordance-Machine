from concordance_machine import ConcordanceMachine

cm = ConcordanceMachine(books=['Romans', 'James'])

cm.get_html_files()
print(cm.html_files)

cm.read_html_files()

print(cm.verses)

cm.generate_concordance()

print(cm.concordance)

cm.print_concordance(type="phrase")
# cm.print_concordance()