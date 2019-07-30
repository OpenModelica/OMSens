model GoodwinKeen "model"
    parameter Real piS=10;
    parameter Real employmentRateZero=0.6;
    parameter Real employmentRateStable=10;
    parameter Real deltaKReal=0.05;
    parameter Real piZ=0.04;
    parameter Real rateInterestOnLoans=0.04;
    parameter Real velocityOfMoney=3;
    parameter Real Betaa=0.015;
    parameter Real Alphaa=0.025;
    parameter Real Capital_init=300;
    parameter Real Debt_init=0;
    parameter Real LaborProductivity_init=1;
    parameter Real Population_init=150;
    parameter Real wageRate_init=0.8;
    
    Real Interest=(rateInterestOnLoans)*(Debt);
    Real Output=(Capital)/((velocityOfMoney));
    Real Labor=(Output)/((LaborProductivity));
    Real Wages=(wageRate)*(Labor);
    Real employmentRateValue=(Labor)/((Population));
    Real wageFunction=(employmentRateStable)*(employmentRateValue-(employmentRateZero));
    Real ProfitGrossReal=Output-(Wages);
    Real omega=(Wages)/((Output));
    Real ProfitNet=(ProfitGrossReal)-(Interest);
    Real piR=(ProfitNet)/((Capital));
    Real InvestmentFunctionReal=(piR-(piZ))*(piS);
    Real InvestmentGross=(InvestmentFunctionReal)*(Output);
    Real InvestmentNetReal=InvestmentGross-((Capital)*(deltaKReal));
    
    Real Capital(start=Capital_init);
    Real Debt(start=Debt_init);
    Real LaborProductivity(start=LaborProductivity_init);
    Real Population(start=Population_init);
    Real wageRate(start=wageRate_init);
initial equation
    Capital=Capital_init;
    Debt=Debt_init;
    LaborProductivity=LaborProductivity_init;
    Population=Population_init;
    wageRate=wageRate_init;
equation
    der(Capital)=InvestmentNetReal;
    der(Debt)=InvestmentGross;
    der(LaborProductivity)=(Alphaa)*(LaborProductivity);
    der(Population)=(Population)*(Betaa);
    der(wageRate)=(wageFunction)*(wageRate);
end GoodwinKeen;