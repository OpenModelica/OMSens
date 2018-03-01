      SUBROUTINE ZXPOWL(F,EPS,N,X,FMIN,ITMAX,WA,IER)
C     ZXPOWL
C.ZXPOWL.................S/D............................................
C
C     FUNCTION          - POWELL'S ALGORITHM TO FIND A (LOCAL) MINIMUM
C                         OF A REAL FUNCTION OF N REAL VARIABLES
C     USAGE             - CALL ZXPOWL (F,EPS,N,X,FMIN,ITMAX,WA,IER)
C     PARAMETER   F     - A FUNCTION SUBPROGRAM WRITTEN BY THE USER
C                 EPS   - CONVERGENCE CRITERION - SEE ELEMENT
C                            DO
C                 N     - LENGTH OF THE VECTOR ARRAY X (INPUT)
C                 X     - A VECTOR ARRAY OF LENGTH N. ON INPUT, X IS AN
C                           INITIAL GUESS FOR THE MINIMUM, ON OUTPUT
C                          X IS THE COMPUTED MINIMUM POINT
C                 FMIN- - F(X)-FUNCTION F EVALUATED AT X OPTIMUM
C                 ITMAX - ON INPUT = THE MAXIMUM ALLOWABLE NUMBER OF
C                         ITERATIONS PER ROOT AND ON OUTPUT = THE
C                         NUMBER OF ITERATIONS USED
C                 IER   - ERROR PARAMETER (OUTPUT)
C                 WA    - AUXILIARY VECTOR. MUST BE DECLARED IN THE MAIN
C                            PROGRAM WITH DIMENSION N(N+4)
C                         TERMINAL ERROR = 128+N
C                         N = 1 NO FINITE MINIMUM OBTAINED
C                         N = 2 F IS LEVEL ALONG A LINE THROUGH X
C                         N = 4 FAILURE TO CONVERGE IN ITMAX
C                               ITERATIONS
C                         N = 8 GRADIENT 'LARGE' AT CALCULATED MINIMUM
C  NUEVO DESDE ACA:
C                          IERROR=140 (no se que N es) es porque hubo division por 0
C  NUEVO HASTA ACA:
C    AUTHOR/IMPLEMENTER - O. G. JOHNSON/L. L. WILLIAMS
C    PRECISION                  DOUBLE
      DOUBLE PRECISION X(1),WA(1),F,FMIN,FS,FB,FL,DB,HX,DM,
     *DQ,HQ,HD,DC,FM,FC,DA,FA,EPS
C     LANGUAGE               - FORTRAN
C...................................................
C     LATEST REVISION - MARCH 22, 1971
C
C	30/05/2003: Statement in line 90 has been modified from the original version
C
C
      IER = 0
      ISW3 = 0
      N2 = N*N
      ID = N2
      IP = ID+N
      IS = IP+N
      IT = IS+N
      DO 5 K=1,N
      IPK = IP +K
      WA(IPK) = X(K)
      ITK = IT + K
5     WA(ITK) = 1.
C                             COMPUTE FIRST FUNCTION VALUE
      FS = F(WA(IP+1))
	    ! write(6,1000)FS,EPS,n
	    write(1,1000)FS,EPS,n
1000  format(/,' === First function value en ZXPOWL = ',d16.8,
     *' EPS = ',d16.8,' n = ',i3)
C                                        pause
      FB = FS
      I = 1
      IC = 1
      ITT = 0
      M = 0
      MF = 0
      ISW1 = 1
10    ITT = ITT+1
      FL = FS
      DO 15 K=1,N
      IDK = ID + K
15    WA (IDK) = 0.
      IDD = I
      I = IC
      ISW2 = 0
20    NS = 0
      IPP = 0
      DB = 0.
      IPI = IP + I
      IF (ISW2 .EQ. 0) HX = WA(IPI)
      IF ((ITT .NE. 1) .OR. (ISW1 .NE. 1)) GO TO 25
      DM = .1
C1    IF (DABS(HX) .GT. 1.) DM = -DM*HX
      IF (DABS(HX) .GT. 1.D0) DM = -DM*HX
      GO TO 75
25    IF (ISW1 .NE. 2) GO TO 30
      DM = DQ
      IF (ITT .EQ. 1) DM = HQ
      GO TO 75
30    ITI = IT + I
      HD = WA(ITI)

C2	Original statement:
C2    IF (ISW2 .EQ. 1) HD = WA(IS+1)

C2	Modified statement:
      IF (ISW2 .EQ. 1) HD = WA(IS+I)
      DC = HQ
      IF (ITT .EQ. 2)DC=0.01
      DM = DC
      ASSIGN 35 TO IMRK
      GO TO 120
35    DM=0.5*DC-(FM-FB)/(DC*HD)
      IF(FM .GE. FB)GO TO 40
      FC = FB
      FB = FM
      DB = DC
      IF (DM .EQ. DB) GO TO 160
      DC = 0.
      GO TO 50
40    IF (DM .NE. DB) GO TO 45
      DA = DC
      FA = FM
      GO TO 70
45    FC = FM
50    ASSIGN 55 TO IMRK
      GO TO 120
C                               ANALYZE NEW FUNCTION VALUE
55    IF (FM .LT. FB) GO TO 60
      DA = DM
      FA = FM
      GO TO 65
60    DA = DB
      FA = FB
      DB = DM
      FB = FM
65    IF((DC-DA)/(DB-DA) .GT. 0.0) GO TO 115
      IF (DB .NE. 0.0) GO TO 160
70    NS = 1
      DM = -DC
75    IF (NS .LE. 15) GO TO 85
      IF (FS .NE. FM) GO TO 80
      DB = 0.
      MF = N+2
      GO TO 160
C1    80 IF (DABS(DM) .LE. 10.E5) GO TO 85
80    IF (DABS(DM) .LE. 10.D5) GO TO 85
      ISW3 = 1
      GO TO 160
85    NS = NS + 1
      ASSIGN 90 TO IMRK
      GO TO 120
90    IF (FM .LT. FB) GO TO 100
      IF (FM .EQ. FB) GO TO 105
      IF (NS .EQ. 1) GO TO 110
95    DC = DM
      FC = FM
      GO TO 115
100   DA = DB
      FA = FB
      DB = DM
      FB = FM
      DM = DM+DM
      GO TO 75
105   IF (FS .EQ. FB) GO TO 100
      IF (NS .NE. 1) GO TO 95
110   DA = DM
      FA = FM
      DM = -DM
      GO TO 75
115   HD=(FC-FB)/(DC-DB)+(FA-FB)/(DB-DA)
      DM=0.5*(DA+DC)+(FA-FC)/(HD+HD)
      IPP=IPP+1
      ASSIGN 140 TO IMRK
120   IF (ISW2 .EQ. 1) GO TO 125
      IPI = IP+I
      WA(IPI) = HX+DM
      GO TO 135
125   DO 130 K=1,N
      IPK = IP+K
      MK = M+K
      WA(IPK) = X(K)+DM*WA(MK)
130   CONTINUE
135   FM = F(WA(IP+1))
      GO TO IMRK,(35, 55, 90, 140)
140   IF (FM .LE. FB) GO TO 150
      IF (IPP .EQ. 3) GO TO 155
C DESDE ACA NUEVO:
C   Si lo de la division de abajo da 0 entonces salgamos de zxpowl, no nos importa nada
      IF ((DM-DB) .EQ. 0.0) GO TO 235
C HASTA ACA NUEVO^
      IF ((DC-DB)/(DM-DB) .GT. 0.0) GO TO 145
      DA = DM
      FA = FM
      GO TO 115
145   DC = DM
      FC = FM
      GO TO 115
150   DB = DM
      FB = FM
155   HD=(HD+HD)/(DC-DA)
      ITI =  IT+I
      IF (ISW2 .NE. 1) WA(ITI) = HD
      ISI = IS+I
      WA(ISI) = HD
      IF (FB .EQ. FS) DB = 0.
160   IF (ISW2 .EQ. 1) GO TO 165
      IDI = ID+I
      WA(IDI) = WA(IDI)+DB
      HD = HX+DB
      IPI = IP+I
      WA(IPI) = HD
      X(I) = HD
      GO TO 175
165   DO 170 K=1,N
      MK = M+K
      HD = DB*WA(MK)
      IDK = ID+K
      WA(IDK) = WA(IDK)+HD
      HD = X(K)+HD
      IPK = IP+K
      WA(IPK)=HD
170   X(K) = HD
175   IF (ISW3 .NE. 1) GO TO 176
      IER = 129
      GO TO 230
176   FS = FB
      IF (I .EQ. N) I=0
      I = I+1
      IF (ISW1 .NE. 0.0) GO TO 185
      IF (DB .NE. 0.0) GO TO 180
      IF (I .NE. IC) GO TO 20
180   IC = I
      ISW1 = 1
      IF (ITT .GT. N) ISW2 = 1
      I = IDD
      GO TO 20
185   M = M+N
      IF (M .EQ. N2) M=0
      IF (ISW1 .NE. 1) GO TO 205
      IF (I .EQ. 1) ISW2 = 1
      IF (I .NE. IDD) GO TO 20
      HQ = 0.
      DO 190 K=1,N
      IDK = ID+K
      HQ = HQ+WA(IDK)**2
190   CONTINUE
      IF (HQ .NE. 0.0) GO TO 195
      IF (MF .GT. (N+1)) IER = 130
      GO TO 230
195   DQ = DSQRT(HQ)
      HQ = DMIN1(1.D0,DQ)
      DO 200 K=1,N
      MK = M+K
      IDK = ID+K
      WA(MK) = WA(IDK)/DQ
200   CONTINUE
      ISW1 = 2
      GO TO 20
205   ISW1 = 0
      IF ((FL-FS) .LE. (EPS*DMAX1(1.D0,DABS(FS)))) GO TO 215
206   IF (ITT .GT. ITMAX) GO TO 210
      MF = 0
      GO TO 10
210   IER = 132
      GO TO 230
215   IF (MF .LE. (N+1)) GO TO 220
      IER = 130
      GO TO 230
220   MF = MF+1
      DQ = 0.
      DO 225 K=1,N
      IDK = ID+K
      IPK = IP+K
      DQ = DQ+DABS(WA(ID+K))/DMAX1(1.D0,DABS(WA(IP+K)))
225   CONTINUE
      IF (DQ .LE. N*EPS) GO TO 230
      IF (MF .LE. N) GO TO 10
      IER = 136
C Desde aca nuevo:
      GO TO 230
235   IER = 140
      write(*,*) "----------------"
      write(*,*) "ENTRO A DONDE NO TENÍA QUE ENTRAR."
      write(*,*) "   VOY A IGNORAR EL ERROR DE ZXPOWL"
      write(*,*) "----------------"
      write(*,*) ""
C Hasta aca nuevo^
230   FMIN = FB
      ITMAX = ITT
      IF (IER .NE. 0) GO TO 9000
9000  CONTINUE

      ! write(6,9010)FMIN
	     write(1,9010)FMIN
9010   format(/,' ======== FMIN = ',d16.8)
C       pause 7
      RETURN
      END SUBROUTINE ZXPOWL
