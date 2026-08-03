#pragma TextEncoding = "UTF-8"
#pragma rtGlobals = 3

// ---- Espectro largo · 9 categóricos + rampa de 21 pasos --------
// Original de la paleta MGJ. El paquete de Python (mgjstyle) es un port
// uno-a-uno de estas dos tablas: mismos colores, mismo orden.

Function MGJ_MakeColorTables()
	NewDataFolder/O root:Packages
	NewDataFolder/O/S root:Packages:MGJcolors

	Make/O/N=(9,3)/W/U MGJ_Cat
	MGJ_Cat[0][0]= 14649;	MGJ_Cat[0][1]= 5140;	MGJ_Cat[0][2]= 16191	// #39143F
	MGJ_Cat[1][0]= 3855;	MGJ_Cat[1][1]= 26985;	MGJ_Cat[1][2]= 46517	// #0F69B5
	MGJ_Cat[2][0]= 26214;	MGJ_Cat[2][1]= 42919;	MGJ_Cat[2][2]= 51657	// #66A7C9
	MGJ_Cat[3][0]= 33153;	MGJ_Cat[3][1]= 36237;	MGJ_Cat[3][2]= 10537	// #818D29
	MGJ_Cat[4][0]= 65278;	MGJ_Cat[4][1]= 51400;	MGJ_Cat[4][2]= 12336	// #FEC830
	MGJ_Cat[5][0]= 38550;	MGJ_Cat[5][1]= 2827;	MGJ_Cat[5][2]= 0	// #960B00
	MGJ_Cat[6][0]= 14906;	MGJ_Cat[6][1]= 25186;	MGJ_Cat[6][2]= 24672	// #3A6260
	MGJ_Cat[7][0]= 21074;	MGJ_Cat[7][1]= 1285;	MGJ_Cat[7][2]= 6682	// #52051A
	MGJ_Cat[8][0]= 35723;	MGJ_Cat[8][1]= 37008;	MGJ_Cat[8][2]= 33667	// #8B9083

	Make/O/N=(21,3)/W/U MGJ_Seq
	MGJ_Seq[0][0]= 6682;	MGJ_Seq[0][1]= 2827;	MGJ_Seq[0][2]= 11822	// #1A0B2E
	MGJ_Seq[1][0]= 10280;	MGJ_Seq[1][1]= 4112;	MGJ_Seq[1][2]= 16191	// #28103F
	MGJ_Seq[2][0]= 14392;	MGJ_Seq[2][1]= 5140;	MGJ_Seq[2][2]= 20817	// #381451
	MGJ_Seq[3][0]= 19275;	MGJ_Seq[3][1]= 6168;	MGJ_Seq[3][2]= 23901	// #4B185D
	MGJ_Seq[4][0]= 24672;	MGJ_Seq[4][1]= 7196;	MGJ_Seq[4][2]= 25700	// #601C64
	MGJ_Seq[5][0]= 30069;	MGJ_Seq[5][1]= 8481;	MGJ_Seq[5][2]= 27499	// #75216B
	MGJ_Seq[6][0]= 35466;	MGJ_Seq[6][1]= 10280;	MGJ_Seq[6][2]= 27242	// #8A286A
	MGJ_Seq[7][0]= 40606;	MGJ_Seq[7][1]= 12079;	MGJ_Seq[7][2]= 26985	// #9E2F69
	MGJ_Seq[8][0]= 45232;	MGJ_Seq[8][1]= 15163;	MGJ_Seq[8][2]= 25957	// #B03B65
	MGJ_Seq[9][0]= 49344;	MGJ_Seq[9][1]= 19275;	MGJ_Seq[9][2]= 23901	// #C04B5D
	MGJ_Seq[10][0]= 53456;	MGJ_Seq[10][1]= 23130;	MGJ_Seq[10][2]= 21845	// #D05A55
	MGJ_Seq[11][0]= 56026;	MGJ_Seq[11][1]= 28270;	MGJ_Seq[11][2]= 20560	// #DA6E50
	MGJ_Seq[12][0]= 58339;	MGJ_Seq[12][1]= 33153;	MGJ_Seq[12][2]= 18761	// #E38149
	MGJ_Seq[13][0]= 60395;	MGJ_Seq[13][1]= 37779;	MGJ_Seq[13][2]= 18504	// #EB9348
	MGJ_Seq[14][0]= 61423;	MGJ_Seq[14][1]= 41891;	MGJ_Seq[14][2]= 20303	// #EFA34F
	MGJ_Seq[15][0]= 62708;	MGJ_Seq[15][1]= 46260;	MGJ_Seq[15][2]= 21845	// #F4B455
	MGJ_Seq[16][0]= 63479;	MGJ_Seq[16][1]= 50115;	MGJ_Seq[16][2]= 27242	// #F7C36A
	MGJ_Seq[17][0]= 63736;	MGJ_Seq[17][1]= 53970;	MGJ_Seq[17][2]= 32639	// #F8D27F
	MGJ_Seq[18][0]= 64250;	MGJ_Seq[18][1]= 57054;	MGJ_Seq[18][2]= 38293	// #FADE95
	MGJ_Seq[19][0]= 64764;	MGJ_Seq[19][1]= 59367;	MGJ_Seq[19][2]= 44718	// #FCE7AE
	MGJ_Seq[20][0]= 65021;	MGJ_Seq[20][1]= 61680;	MGJ_Seq[20][2]= 50886	// #FDF0C6

	SetDataFolder root:
End

// Aplica la categórica a las trazas del gráfico activo
Function MGJ_ColorTraces()
	Wave/Z ct = root:Packages:MGJcolors:MGJ_Cat
	if (!WaveExists(ct))
		MGJ_MakeColorTables()
		Wave ct = root:Packages:MGJcolors:MGJ_Cat
	endif
	String list = TraceNameList("", ";", 1)
	Variable i, n = ItemsInList(list), rows = DimSize(ct, 0)
	for (i = 0; i < n; i += 1)
		Variable k = mod(i, rows)
		ModifyGraph rgb($StringFromList(i, list)) = (ct[k][0], ct[k][1], ct[k][2])
	endfor
End

// Rampa continua: interpola la secuencial sobre N trazas
Function MGJ_RampTraces()
	Wave/Z sq = root:Packages:MGJcolors:MGJ_Seq
	if (!WaveExists(sq))
		MGJ_MakeColorTables()
		Wave sq = root:Packages:MGJcolors:MGJ_Seq
	endif
	String list = TraceNameList("", ";", 1)
	Variable i, n = ItemsInList(list), last = DimSize(sq, 0) - 1
	for (i = 0; i < n; i += 1)
		Variable p = (n > 1) ? i / (n - 1) * last : 0
		Variable lo = floor(p), hi = min(lo + 1, last), f = p - lo
		ModifyGraph rgb($StringFromList(i, list)) = (sq[lo][0]*(1-f) + sq[hi][0]*f, sq[lo][1]*(1-f) + sq[hi][1]*f, sq[lo][2]*(1-f) + sq[hi][2]*f)
	endfor
End
