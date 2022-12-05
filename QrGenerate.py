import qrcode
code = qrcode.make('Merah')
code1 = qrcode.make('Kuning')
code2 = qrcode.make('Hijau')
code3 = qrcode.make('Biru')

code.save('TrajectoryMerah.png')
code1.save('TrajectoryKuning.png')
code2.save('TrajectoryHijau.png')
code3.save('TrajectoryBiru.png')