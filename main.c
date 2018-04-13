/* ###################################################################
**     Filename    : main.c
**     Project     : Ozuna
**     Processor   : MC9S08QE128CLK
**     Version     : Driver 01.12
**     Compiler    : CodeWarrior HCS08 C Compiler
**     Date/Time   : 2018-01-29, 15:53, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.12
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */


/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "Bit1.h"
#include "Bit2.h"
#include "Bit3.h"
#include "Bit4.h"
#include "Bit5.h"
#include "AS1.h"
#include "TI1.h"
#include "AD1.h"
/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"

unsigned char estado;
unsigned int Enviados = 2;
unsigned int Enviados2 = 5;
unsigned char CodError;
unsigned char CodError1;
bool D1=FALSE;
bool D2=FALSE;


//Variables de la comunicación con Arduino
unsigned char Data_Arduino[1]= 0x00;
unsigned int l_Arduino = 1;
//

//Variables de medida para aplicar el protocolo de comunicación
typedef union{
unsigned char u8[2];
unsigned int u16;
}amplitud;

volatile amplitud iADC1;
volatile amplitud iADC2;

unsigned char dTrama[5]={0xF1,0x00,0x00,0x00,0x00};			// Trama de salida a la PC


/* User includes (#include below this line is not maintained by Processor Expert) */

void main(void)
{
  /* Write your local variable definition here */

  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
  PE_low_level_init();
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
  /* For example: for(;;) { } */
  for(;;){
	  switch(estado){
	  
	  case ESPERAR:
		  break;

	  
	  case MEDIR:
	    			CodError = AD1_MeasureChan(TRUE, 0);			//Medida del canal 0 Sharp
	    			CodError = AD1_GetChanValue16(0, &iADC1.u16);
	    			
	    			iADC2.u8[1]=Data_Arduino[0];					//Medida del Giroscopio
	    			iADC2.u8[0]= 0x00;
	    			  
	    			D1 = Bit5_GetVal(); 							//Medida sensor Digital knoc
	    			D2 = Bit4_GetVal(); 							//Medida sensor Digital Efecto Hall
	    			
	    			estado = ENVIAR;
	    			break;
		  
	  case ENVIAR:
		  
		  //Protocolo de Comunicación, En la posición 0 se guarda el encabezado de la trama
		  
		  //Sensores Analógicos
		  dTrama[2] = ((iADC1.u16 >> 4) &(0x7F));	//Byte 2 y 3 (D1, D2 Y A1) Sharp
		  dTrama[1] = ((iADC1.u16 >> 11)&(0x1F));
		  
		  dTrama[4] = ((iADC2.u16)&(0x7F));			//Byte 3 y 4 (D3, D4 y A2) Giroscopo
		  dTrama[3] = ((iADC2.u16 >> 7)&(0x1F));
		  
		  //Sensores Digitales
		  if(!D1){
			  dTrama[1] = dTrama[1]|(0x40);
		  }
		  if(!D2){
		  			  dTrama[1] = dTrama[1]|(0x20);
		  		  }
		  
		CodError = AS1_SendBlock(dTrama, 5, &Enviados2);
		estado = ESPERAR;
		break;
		
	  default:
		  break;
	  }
  }

  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** RTOS startup code. Macro PEX_RTOS_START is defined by the RTOS component. DON'T MODIFY THIS CODE!!! ***/
  #ifdef PEX_RTOS_START
    PEX_RTOS_START();                  /* Startup of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of RTOS startup code.  ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.3 [05.09]
**     for the Freescale HCS08 series of microcontrollers.
**
** ###################################################################
*/
