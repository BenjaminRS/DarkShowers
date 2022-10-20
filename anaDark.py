import numpy
import ROOT
from ROOT import *
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()
from DataFormats.FWLite import Events, Handle

### IO ###
xrd="root://xrootd-cms.infn.it/"
ctaus=[1,10,50,100,500]
masses=[2,20]
input=[]
hist={}
count=0
totcount=0

### Objects from file ###
GenPs, GenPLabel = Handle("std::vector<reco::GenParticle>"),["genParticles","","SIM"]

for m in masses:
    for c in ctaus:
        # for x in range(50):
        for x in range(1): #Test: look at 1 file per phase point
            input.append("/store/user/mcitron/ProjectMetis/HiddenValley_vector_m_{mass}_ctau_{ctau}_xiO_1_xiL_1_privateMC_11X_GENSIM_v3_generationForBParking/output_{file}.root".format(mass=m,ctau=c,file=x+1))
        outName='Hist_m'+str(m)+'_c'+str(c)+'.root'
        outputFile = TFile(outName,'RECREATE')

        ### Histograms ###
        hist["genDaughterID_m{mass}_c{ctau}".format(mass=m,ctau=c)]=TH1D("genDaughterID_m"+str(m)+"_c"+str(c),"genDaughterID_m"+str(m)+"_c"+str(c),200,-100.0,100.0)
        hist["genDaughterPt_m{mass}_c{ctau}".format(mass=m,ctau=c)]=TH1D("genDaughterPt_m"+str(m)+"_c"+str(c),"genDaughterPt_m"+str(m)+"_c"+str(c),2000,0.0,200.0)
        hist["genDaughterEta_m{mass}_c{ctau}".format(mass=m,ctau=c)]=TH1D("genDaughterEta_m"+str(m)+"_c"+str(c),"genDaughterEta_m"+str(m)+"_c"+str(c),500,-2.5,2.5)
        hist["genDaughterPhi_m{mass}_c{ctau}".format(mass=m,ctau=c)]=TH1D("genDaughterPhi_m"+str(m)+"_c"+str(c),"genDaughterPhi_m"+str(m)+"_c"+str(c),640,-3.2,3.2)
        hist["genDaughterR_m{mass}_c{ctau}".format(mass=m,ctau=c)]=TH1D("genDaughterR_m"+str(m)+"_c"+str(c),"genDaughterR_m"+str(m)+"_c"+str(c),5000,0.0,5000.0)

        ### Events loop ###
        for f in input:
            print("File: ",f)
            events = Events(xrd+f)    #Use xrootd
            for nEv,event in enumerate(events):
                count+=1
                totcount+=1
                if count>=100: break
                if (count%50==0): print("Event: ",count)
                try:
                    event.getByLabel(GenPLabel,GenPs)
                except RuntimeError:
                    print("No Gen Particles")
                ### GenPs ###
                for i,gen in enumerate(GenPs.product()):
                    # if i>=10: break
                    if (gen.pdgId()==4900113):
                        r=sqrt(gen.vx() * gen.vx() + gen.vy() * gen.vy())
                        for d in range(gen.numberOfDaughters()):
                            dau=gen.daughter(d)
                            rdau=sqrt(dau.vx() * dau.vx() + dau.vy() * dau.vy())
                            # print("\tDau [{i}] pt: {genPt:7.2f}\tq: {genQ}\teta: {genE:7.2f}\tphi: {genP:7.2f}\tID: {genID}\tstatus: {genS}\tvx: {vx:7.3f}\tvy: {vy:7.3f}\tr: {r:7.3f}".format(i=d,genPt=dau.pt(),genQ=dau.charge(),genE=dau.eta(),genP=dau.phi(),genID=dau.pdgId(),genS=dau.status(),vx=dau.vx(),vy=dau.vy(),r=rdau))
                            hist["genDaughterID_m{mass}_c{ctau}".format(mass=m,ctau=c)].Fill(dau.pdgId())
                            hist["genDaughterPt_m{mass}_c{ctau}".format(mass=m,ctau=c)].Fill(dau.pt())
                            hist["genDaughterEta_m{mass}_c{ctau}".format(mass=m,ctau=c)].Fill(dau.eta())
                            hist["genDaughterPhi_m{mass}_c{ctau}".format(mass=m,ctau=c)].Fill(dau.phi())
                            hist["genDaughterR_m{mass}_c{ctau}".format(mass=m,ctau=c)].Fill(rdau)
            # if count>=1000: break
            count=0
        outputFile.cd()
        hist["genDaughterID_m{mass}_c{ctau}".format(mass=m,ctau=c)].Write()
        hist["genDaughterPt_m{mass}_c{ctau}".format(mass=m,ctau=c)].Write()
        hist["genDaughterEta_m{mass}_c{ctau}".format(mass=m,ctau=c)].Write()
        hist["genDaughterPhi_m{mass}_c{ctau}".format(mass=m,ctau=c)].Write()
        hist["genDaughterR_m{mass}_c{ctau}".format(mass=m,ctau=c)].Write()
        outputFile.Close()
        input.clear()
print(totcount," events processed")
