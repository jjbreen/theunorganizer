import math

def reproject(point, rotate, zero, bounds, imsize):
	rotate = rotate*math.PI/180.0;
	point = [point[0], -point[1]]; 
	point = [point[0] * math.cos(rotate) + point[1] * math.sin(rotate), -point[0] * math.sin(rotate) + point[1] * math.cos(rotate)];

	point = [point[0]+zero[0], -(point[1]-zero[1])]; 
	rrpoint = [(point[0] / imsize[0]), point[1] / imsize[1]];
	return [bounds[0] + (bounds[2]-bounds[0])*rrpoint[0], bounds[3] + (bounds[1]-bounds[3])*rrpoint[1]];

allData = [{"name":"AK0.png",
	"rooms":[
		{"point":[370,653],"name":"27"},
		{"point":[510,1143],"name":"26"},
		{"point":[213,1210],"name":"24a"},
		{"point":[490,1463],"name":"25"},
		{"point":[103,1580],"name":"24d"},
		{"point":[213,2206],"name":"20"},
		{"point":[223,2520],"name":"19"},
		{"point":[293,3033],"name":"18"},
		{"point":[1027,3123],"name":"16"},
		{"point":[923,2610],"name":"14"},
		{"point":[1160,2243],"name":"13"},
		{"point":[3705,3100],"name":"9"},
		{"point":[3669,2780],"name":"10"},
		{"point":[3662,2536],"name":"11"},
		{"point":[3652,2186],"name":"12"},
		{"point":[4085,2243],"name":"5"},
		{"point":[4109,2533],"name":"6"},
		{"point":[4095,2776],"name":"7"},
		{"point":[4092,2990],"name":"8"},
		{"point":[4419,2626],"name":"4"},
		{"point":[4575,1826],"name":"3"},
		{"point":[4385,940],"name":"1"},
		{"point":[3882,843],"name":"1b"},
		{"point":[3615,813],"name":"1a"},
		{"point":[3452,923],"name":"2"}]},
{"name":"AK1.png",
	"rooms":[
		{"point":[1055,577],"name":"108"},
		{"point":[1625,740],"name":"107"},
		{"point":[1772,467],"name":"106"},
		{"point":[2065,490],"name":"105"},
		{"point":[2285,557],"name":"104"},
		{"point":[2452,520],"name":"103"},
		{"point":[2715,547],"name":"102"},
		{"point":[2935,547],"name":"101"},
		{"point":[4072,1153],"name":"111a"},
		{"point":[4252,1667],"name":"112"},
		{"point":[3635,1240],"name":"111"},
		{"point":[3912,1900],"name":"112e"},
		{"point":[3529,1893],"name":"112f"},
		{"point":[3982,2133],"name":"112d"},
		{"point":[3475,2120],"name":"114"},
		{"point":[2692,2120],"name":"115"},
		{"point":[2215,2053],"name":"117"},
		{"point":[1972,2047],"name":"118"},
		{"point":[1712,1860],"name":"113b"},
		{"point":[1722,1513],"name":"113a"},
		{"point":[2382,1613],"name":"113"},
		{"point":[2375,1157],"name":"132"},
		{"point":[1113,1187],"name":"109"},
		{"point":[643,1163],"name":"109a"},
		{"point":[203,1153],"name":"120e"},
		{"point":[390,1650],"name":"120d"},
		{"point":[1147,1690],"name":"120c"},
		{"point":[723,2110],"name":"120a"},
		{"point":[100,2127],"name":"121"},
		{"point":[193,2450],"name":"122"},
		{"point":[150,2777],"name":"124"},
		{"point":[150,3110],"name":"125"},
		{"point":[113,3367],"name":"126a"},
		{"point":[120,3597],"name":"126"},
		{"point":[627,3643],"name":"127"},
		{"point":[1110,3553],"name":"128"},
		{"point":[1093,3133],"name":"129"},
		{"point":[1127,2757],"name":"130"},
		{"point":[627,3207],"name":"131"},
		{"point":[620,2880],"name":"123"},
		{"point":[1250,2130],"name":"120b"},
		{"point":[4100,3314],"name":"116"}]},
{"name":"AK2.png",
	"rooms":[
		{"point":[1047,3054],"name":"233"},
		{"point":[410,3451],"name":"232"},
		{"point":[313,2987],"name":"231"},
		{"point":[347,2704],"name":"230"},
		{"point":[320,2401],"name":"229"},
		{"point":[340,2017],"name":"228"},
		{"point":[650,1381],"name":"227"},
		{"point":[873,2004],"name":"226"},
		{"point":[1237,1957],"name":"225"},
		{"point":[1303,1457],"name":"207a"},
		{"point":[1840,2014],"name":"224"},
		{"point":[2877,2021],"name":"221"},
		{"point":[2990,1607],"name":"211b"},
		{"point":[2980,1207],"name":"211a"},
		{"point":[2440,1467],"name":"210"},
		{"point":[2120,1401],"name":"209"},
		{"point":[2157,1781],"name":"209a"},
		{"point":[1840,1457],"name":"208b"},
		{"point":[1897,1077],"name":"208a"},
		{"point":[3546,1236],"name":"212"},
		{"point":[3623,1713],"name":"212c"},
		{"point":[4316,1386],"name":"212"},
		{"point":[3766,1956],"name":"220"},
		{"point":[4219,1979],"name":"213"},
		{"point":[4669,1969],"name":"214"},
		{"point":[4706,2359],"name":"215"},
		{"point":[4709,2689],"name":"216"},
		{"point":[4739,2939],"name":"217"},
		{"point":[4639,3387],"name":"218"},
		{"point":[4063,3171],"name":"219"},
		{"point":[3729,367],"name":"201"},
		{"point":[3479,580],"name":"200b"},
		{"point":[3276,603],"name":""},
		{"point":[3276,603],"name":"200a"},
		{"point":[2786,483],"name":"202"},
		{"point":[2076,487],"name":"203"},
		{"point":[1799,420],"name":"204"},
		{"point":[1539,413],"name":"205"},
		{"point":[1153,430],"name":"206"}]},
{"name":"AK3.png",
	"rooms":[
		{"point":[520,3441],"name":"323a"},
		{"point":[490,2951],"name":"323"},
		{"point":[247,2421],"name":"322"},
		{"point":[343,2094],"name":"321"},
		{"point":[1357,2424],"name":"325"},
		{"point":[2577,2451],"name":"326"},
		{"point":[3583,2408],"name":"327"},
		{"point":[4297,1614],"name":"315"},
		{"point":[3593,1954],"name":"316"},
		{"point":[3007,1561],"name":"317a"},
		{"point":[2530,1578],"name":"317b"},
		{"point":[2053,1618],"name":"316"},
		{"point":[623,1601],"name":"320"},
		{"point":[1480,1684],"name":"320c"},
		{"point":[1483,1124],"name":"319"},
		{"point":[1197,958],"name":"312"},
		{"point":[3567,1188],"name":"314"},
		{"point":[3947,1001],"name":"313"},
		{"point":[3937,514],"name":"301a"},
		{"point":[3627,501],"name":"301"},
		{"point":[3427,528],"name":"302"},
		{"point":[3177,574],"name":"303"},
		{"point":[2983,571],"name":"304"},
		{"point":[2773,601],"name":"305"},
		{"point":[2503,594],"name":"306"},
		{"point":[2293,594],"name":"307"},
		{"point":[2037,544],"name":"308"},
		{"point":[1867,561],"name":"309"},
		{"point":[1613,581],"name":"310"},
		{"point":[1210,641],"name":"311"}]},
{"name":"CC1.png",
	"rooms":[
		{"point":[240,357],"name":"123"},
		{"point":[627,280],"name":"124"},
		{"point":[317,810],"name":"122"},
		{"point":[1190,453],"name":"126a"},
		{"point":[1147,710],"name":"120"},
		{"point":[1123,1053],"name":"127"},
		{"point":[1690,697],"name":"120"},
		{"point":[1240,1510],"name":"126"},
		{"point":[173,2667],"name":"112"},
		{"point":[1117,3456],"name":"101"},
		{"point":[200,3666],"name":"110"},
		{"point":[577,3656],"name":"109"},
		{"point":[3052,3722],"name":"147"},
		{"point":[5079,3716],"name":"144"},
		{"point":[3506,3406],"name":"154"},
		{"point":[4569,2729],"name":"139"},
		{"point":[4192,2649],"name":"145"},
		{"point":[3892,2692],"name":"151"},
		{"point":[3282,2712],"name":"153"},
		{"point":[2869,2662],"name":"155"}]},
{"name":"CC2.png",
	"rooms":[
		{"point":[847,563],"name":"223"},
		{"point":[600,557],"name":"221"},
		{"point":[263,517],"name":"220"},
		{"point":[240,923],"name":"222"},
		{"point":[693,870],"name":"217"},
		{"point":[743,1227],"name":"218"},
		{"point":[267,1283],"name":"219"},
		{"point":[1840,557],"name":"227"},
		{"point":[1200,783],"name":"226"},
		{"point":[1867,820],"name":"228"},
		{"point":[1850,1093],"name":"230"},
		{"point":[1333,1193],"name":"232"},
		{"point":[1687,1417],"name":"231"},
		{"point":[1470,1463],"name":"233"},
		{"point":[1167,1487],"name":"234"},
		{"point":[380,2243],"name":"207"},
		{"point":[823,3183],"name":"203"},
		{"point":[1927,3603],"name":"204"},
		{"point":[1783,3940],"name":"206"},
		{"point":[2090,3896],"name":"207"},
		{"point":[2517,3906],"name":"208"},
		{"point":[2537,3560],"name":"205"},
		{"point":[3523,3460],"name":"201"},
		{"point":[5000,3610],"name":"248"},
		{"point":[5143,3023],"name":"245"},
		{"point":[4327,2800],"name":"250"},
		{"point":[4887,2566],"name":"241"}]},
{"name":"CC3.png",
	"rooms":[
		{"point":[493,270],"name":"316"},
		{"point":[203,503],"name":"315"},
		{"point":[557,667],"name":"312"},
		{"point":[127,933],"name":"314"},
		{"point":[587,997],"name":"313"},
		{"point":[1373,593],"name":"315"},
		{"point":[1117,967],"name":"324"},
		{"point":[1353,1020],"name":"323"},
		{"point":[1693,937],"name":"320"},
		{"point":[1507,1247],"name":"325"},
		{"point":[1167,1647],"name":"327"},
		{"point":[460,1940],"name":"304"},
		{"point":[773,2947],"name":"301"},
		{"point":[1693,3622],"name":"340"},
		{"point":[2217,3069],"name":"341"},
		{"point":[3057,3082],"name":"342"},
		{"point":[3760,3069],"name":"343"},
		{"point":[4916,3572],"name":"340"},
		{"point":[4386,3272],"name":"345"},
		{"point":[4986,3042],"name":"332"},
		{"point":[3116,1716],"name":"331"}]},
{"name":"FL2.png",
	"rooms":[
		{"point":[3509,443],"name":"246-Beckett"},
		{"point":[4356,4029],"name":"222"},
		{"point":[2576,1733],"name":"fllower"},
		{"point":[2592,3143],"name":"flupper"}]},
{"name":"FL3.png",
	"rooms":[
		{"point":[3826,3869],"name":"320"},
		{"point":[3922,1539],"name":"311"}]},
{"name":"FLB.png",
	"rooms":[
		{"point":[853,873],"name":"a021"}]},
{"name":"SH0.png",
	"rooms":[
		{"point":[1000,2722],"name":"1"},
		{"point":[2167,2435],"name":"3"},
		{"point":[1050,1682],"name":"2"},
		{"point":[3113,1382],"name":"6"},
		{"point":[3563,1352],"name":"7"},
		{"point":[4098,1405],"name":"14"},
		{"point":[5128,1345],"name":"13"},
		{"point":[5381,2065],"name":"12"},
		{"point":[5331,2452],"name":"11"},
		{"point":[5358,3005],"name":"10"},
		{"point":[4741,2989],"name":"9b"},
		{"point":[4205,3019],"name":"9a"}]},
{"name":"SH1.png",
	"rooms":[
		{"point":[5013,2752],"name":"108"},
		{"point":[4310,3035],"name":"108a"},
		{"point":[3313,2915],"name":"107"},
		{"point":[3110,2362],"name":"107a"},
		{"point":[2233,2795],"name":"106"},
		{"point":[1393,2952],"name":"105a"},
		{"point":[980,2969],"name":"105b"},
		{"point":[547,2929],"name":"105c"},
		{"point":[143,2929],"name":"105d"},
		{"point":[223,1265],"name":"104a"},
		{"point":[600,1365],"name":"104b"},
		{"point":[990,1365],"name":"104c"},
		{"point":[1273,1362],"name":"103"},
		{"point":[1810,1315],"name":"102b"},
		{"point":[2183,1329],"name":"102a"},
		{"point":[2547,1365],"name":"101"},
		{"point":[4023,1175],"name":"111"},
		{"point":[4726,1355],"name":"109b"},
		{"point":[5253,1495],"name":"109a"}]},
{"name":"SH2.png",
	"rooms":[
		{"point":[900,1565],"name":"202"},
		{"point":[1877,1405],"name":"201a"},
		{"point":[2317,1379],"name":"201b"},
		{"point":[2563,1325],"name":"201c"},
		{"point":[4137,1189],"name":"209"},
		{"point":[4920,1379],"name":"207"},
		{"point":[5493,1382],"name":"206"},
		{"point":[5350,2822],"name":"205"},
		{"point":[4333,2765],"name":"204"},
		{"point":[2900,2779],"name":"203"},
		{"point":[1930,2852],"name":"202e"},
		{"point":[1503,2852],"name":"202d"},
		{"point":[1047,2885],"name":"202c"},
		{"point":[650,2885],"name":"202b"},
		{"point":[193,2885],"name":"202a"}]},
{"name":"SH3.png",
	"rooms":[
		{"point":[2587,2772],"name":"306"},
		{"point":[3757,2892],"name":"307"},
		{"point":[4950,2789],"name":"308"},
		{"point":[4966,1565],"name":"309"},
		{"point":[3800,1239],"name":"310"},
		{"point":[2637,1305],"name":"301"},
		{"point":[563,1459],"name":"304"}]},
{"name":"SL0.png",
	"rooms":[
		{"point":[2730,2185],"name":"11"}]},
{"name":"SL1.png",
	"rooms":[
		{"point":[800,2965],"name":"104"},
		{"point":[2083,3025],"name":"105"},
		{"point":[4020,3172],"name":"112"},
		{"point":[3467,1918],"name":"115"},
		{"point":[2193,1468],"name":"lounge"},
		{"point":[1333,1528],"name":"101"},
		{"point":[2243,835],"name":"108"},
		{"point":[1180,342],"name":"124"},
		{"point":[2460,193],"name":"129"}]},
{"name":"SL2.png",
	"rooms":[
		{"point":[1227,353],"name":"224"},
		{"point":[1843,343],"name":"223"},
		{"point":[1317,1147],"name":"225"},
		{"point":[2187,1577],"name":"219"},
		{"point":[2197,2297],"name":"245"},
		{"point":[1883,2934],"name":"204"},
		{"point":[4343,3101],"name":"214"}]},
{"name":"SL3.png",
	"rooms":[
		{"point":[2953,3274],"name":"305"},
		{"point":[2663,2797],"name":"304"},
		{"point":[3080,2820],"name":"306"},
		{"point":[3400,2820],"name":"306a"},
		{"point":[1403,2284],"name":"328"},
		{"point":[3183,1794],"name":"310"},
		{"point":[3190,1317],"name":"311"},
		{"point":[2257,1654],"name":"322"},
		{"point":[2170,1170],"name":"321"},
		{"point":[3313,890],"name":"312"},
		{"point":[3250,293],"name":"313"},
		{"point":[2203,213],"name":"317"},
		{"point":[2567,310],"name":"316"},
		{"point":[2303,490],"name":"318"}]},
{"name":"SL4.png",
	"rooms":[
		{"point":[1837,300],"name":"406a"},
		{"point":[2747,277],"name":"406b"},
		{"point":[1227,2276],"name":"412"},
		{"point":[1023,2743],"name":"413"},
		{"point":[1243,3236],"name":"414"},
		{"point":[1863,3280],"name":"401"},
		{"point":[2447,3153],"name":"402"}]},
{"name":"SL5.png",
	"rooms":[
		{"point":[530,260],"name":"501"}]},

];