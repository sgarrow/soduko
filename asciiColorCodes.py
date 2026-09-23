# Setup codes for building things that can be put in print strings

ESC_CODE       = '{}'.format( '\x1b' )
TERMINATE_CODE = '{}'.format( '[0'  )

RED_CODE = '{}'.format( '[31' )  # RED
GRN_CODE = '{}'.format( '[32' )  # GREEN
YEL_CODE = '{}'.format( '[33' )  # YELLLOW
WHT_CODE = '{}'.format( '[37' )  # WHITE

BOLD_ON_CODE   = '{}'.format( '1'    )

# Things that can be put in print strings.
# e.g., print('{}{}{}'.format(RED,'hello',OFF)) # print hello in red.
RED = '{}{}m'.format( ESC_CODE, RED_CODE )
GRN = '{}{}m'.format( ESC_CODE, GRN_CODE )
YEL = '{}{}m'.format( ESC_CODE, YEL_CODE )
WHT = '{}{}m'.format( ESC_CODE, WHT_CODE )

RED_BOLD = '{}{};{}m'.format( ESC_CODE, RED_CODE, BOLD_ON_CODE )
GRN_BOLD = '{}{};{}m'.format( ESC_CODE, GRN_CODE, BOLD_ON_CODE )
YEL_BOLD = '{}{};{}m'.format( ESC_CODE, YEL_CODE, BOLD_ON_CODE )
WHT_BOLD = '{}{};{}m'.format( ESC_CODE, WHT_CODE, BOLD_ON_CODE )

OFF = '{}{}m'.format(    ESC_CODE, TERMINATE_CODE           )
#############################################################################
