c----------------------------------------------------------------------
c     Routine transf implements the change of variables for
c     transforming unconstrained problems into contrained ones
c     and viceversa.
c----------------------------------------------------------------------
      subroutine transf(n,nu,z,bl,bu,mar,x,jbound,ier)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c         n:  number of variables.
c        nu:  flag for starting calculations such that if
c             0 analizes the user-supplied data.
c             1 skips the analysis.
c        bl:  vector of lower bounds.
c        bu:  vector of upper bounds.
c       mar:  flag such that if
c             1 transforms the constrained problem into the
c               unconstrained one.
c             2 transforms the unconstrained problem into the
c               constrained one.
c         z:  if mar=1 it contains the current iterate of the constrained
c             problem.
c         x:  if mar=2 it contains the current iterate of the unconstrained
c             problem.
c
c    jbound:  working vector of dimension n defining the sort of
c             constraint for each variable
c             (only used when ibound.ne.0)
c             jbound(i) = 0 if the ith variable has no contraints.
c                         1 if the ith variable has only upper bounds.
c                         2 if the ith variable has only lower bounds.
c                         3 if the ith variable has both upper and
c                           lower bounds.
c    Output:
c
c         x:  if mar = 1 , x is the transform of the input z.
c   or
c         z:  if mar = 2,  z is the transform of the input x.
c
c       ier:  3 if there exists an input error in the constraints;
c             otherwise is not altered.

c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x(n),bl(n),bu(n),z(n),jbound(n)
      data tol/0.10842022d-18/
      if(mar.eq.1)then
c----------------------------------------------------------------------
c     Analize if the user-supplied data is coherent.
c
c     If the given point does not satisfy the constraints it is
c     projected onto the corresponding region.
c----------------------------------------------------------------------
          if(nu.eq.0)then
                    na1=0
                    na2=0
                    do i=1,n
	        if(jbound(i).eq.3)then
                                  if(bu(i).lt.bl(i))then
                                   na2=na2+1
                                  end if
                       end if
                    end do
                    if(na2.ne.0)then
                        ier=3
                        return
                    end if
                    do i=1,n
                        if(jbound(i).ne.0)then
                          if(jbound(i).ne.2)then
                            if(z(i).gt.bu(i))then
                                z(i)=bu(i)
                            end if
                        end if
                        if(jbound(i).gt.1)then
                            if(z(i).lt.bl(i))then
                                z(i)=bl(i)
                            end if
                        end if
                       end if
                    end do
        end if
c----------------------------------------------------------------------
c   Compute the coordinates of the unconstrained transformed problem.
c   if jbound(i)=1,   using   x = dsqrt(bu - z)
c   if jbound(i)=2,   using   x = dsqrt(z - bl)
c   if jbound(i)=3,   using   x = dasin(dsqrt( (z - bl) / (bu - bl )))
c----------------------------------------------------------------------
        do i=1,n
       x(i)=z(i)
            if(jbound(i).eq.3)then
c-------------------------------------------------------------------
                    wa2=bu(i)-bl(i)
                    if( dabs(wa2).gt.tol* dabs((bu(i)+bl(i))/2))then
                             x(i)=dasin(dsqrt((z(i)-bl(i))/wa2))
                    else
                             x(i)=0.d0
                    end if
            else
                    if(jbound(i).eq.1)then
                        x(i)=dsqrt(bu(i)-z(i))
                    else
                        if(jbound(i).eq.2)then
                            x(i)=dsqrt(z(i)-bl(i))
                        end if
                    end if
           end if
        end do
        return
c----------------------------------------------------------------------
c      if mar.ne.1 transform the point x of the unconstrained problem
c      into the corresponding point z of the constrained problem.
c      if jbound(i)=1,   using      z = bu - x**2
c      if jbound(i)=2,   using      z = bl + x**2
c      if jbound(i)=3,   using      z = bl + (bu - bl)* (sin x)**2
c----------------------------------------------------------------------
      else
            do i=1,n
                    if(jbound(i).eq.1)then
                        z(i)=-x(i)**2+bu(i)
                    else
                       if(jbound(i).eq.2)then
                           z(i)=x(i)**2+bl(i)
                       else
                          if(jbound(i).eq.3)then
                              wa2=bu(i)-bl(i)
                              z(i)=bl(i)+wa2*(dsin(x(i)))**2
                          else
                              z(i)=x(i)
                          end if
                       end if
                     end if
             end do
      end if
      return
      end

c  ********************************************************************
c----------------------------------------------------------------------
c  ********************************************************************
c----------------------------------------------------------------------
c     Transf2 changes the current iterate if the unconstrained
c     problem converges to a point which is a stationary one of
c     constrained problem.
c----------------------------------------------------------------------
      subroutine transf2(n,bl,bu,gp,y,x,f,fu,jbound,nfu)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c
c    Input :
c        n : dimension of the problem.
c       bl : vector of lower bounds.
c       bu : vector of upper bounds.
c        y : current iterate of the constarined problem.
c        x : iterate corresponding to y in the unconstrained problem.
c       gp : projected gradient at y.
c       fu : user-supplied function.
c   jbound : see definition in the main routine.
c
c   Output :
c        y : current iterate in the constrained problem.
c        x : current iterate in the unconstrained problem.
c        f : f(y).
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension y(n),x(n),gp(n),bl(n),bu(n),jbound(n)
      external fu
      dn=dnrm2(n,gp,1)
      alf=1.d1/dn
c----------------------------------------------------------------------
c     Calculate the step along the direction -gp.
c----------------------------------------------------------------------
      do i=1,n
              if(gp(i).gt.0.d0)then

              if(jbound(i).eq.3.or.jbound(i).eq.2)then
                      ci=bl(i)+1.d1*dmax1(dabs(bl(i)),1.d0)
                      bet=0.9d0
                      if(jbound(i).eq.3)ci=bu(i)
                      if(y(i)-bl(i).gt.(ci-bl(i))/1.d4)bet=2.d-1
                      alf=dmin1(alf,dmin1(bet*(y(i)-bl(i))/gp(i),alf))
              else
                      alf=dmin1(alf,1.d-3/dn*dmax1(dabs(y(i)),1.d0))
              end if

        end if

        if(gp(i).lt.0.d0) then

              if(jbound(i).eq.3.or.jbound(i).eq.1)then
                      ci=bu(i)-1.d1*dmax1(dabs(bu(i)),1.d0)
                      bet=0.9d0
                      if(jbound(i).eq.3)ci=bl(i)
                      if(bu(i)-y(i).gt.dabs(bu(i)-ci)/1.d4)bet=2.d-1
                      alf=dmin1(alf,bet*(bu(i)-y(i))/(-gp(i)))
              else
                      alf=dmin1(alf,1.d-3/dn*dmax1(dabs(y(i)),1.d0))
              end if

      end if
      end do
c----------------------------------------------------------------------
c     Define y = y - alf *gp in the constrained problem.
c     Compute x, iterate in the unconstrained problem corresponding
c     to y.
c----------------------------------------------------------------------
      do i=1,n
              if(dabs(gp(i)).gt.0.d0)then
                      coe=1.d0
                      y(i)=y(i)-alf*gp(i)
                      if(jbound(i).eq.3) then
                              if(x(i).lt.0.d0)coe=-1.d0
                              x(i)=coe*dasin(dsqrt((y(i)-bl(i))/
     *            (bu(i)-bl(i))))
                      else
                              if(jbound(i).eq.1)then
                             if(x(i).lt.0.d0)coe=-1.d0
                             x(i)=coe*dsqrt(bu(i)-y(i))
                              else
                             if(jbound(i).eq.2)then
                             if(x(i).lt.0.d0)coe=-1.d0
                             x(i)=coe*dsqrt(y(i)-bl(i))
                                      else
                             x(i)=y(i)
                                      end if
                              end if
                      end if
              end if
      end do
c----------------------------------------------------------------------
c     Compute f(y).
c----------------------------------------------------------------------
      call fu(n,y,f)
      nfu=nfu+1
      return
      end
c--------------------------------------------------------------------
c  ********************************************************************
c----------------------------------------------------------------------
c     Gradx computes the gradient of the transformed problem.
c----------------------------------------------------------------------
      subroutine gradx(n,x,bl,bu,gt,gra,jbound)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input :
c
c         n : number of variables.
c         x : current iterate.
c        bl : vector of lower bounds.
c        bu : vector of upper bounds.
c        gt : gradient of the original problem.
c    jbound : see definition in the main routine.
c
c    Output :
c
c       gra : gradient at x.
c---------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x(n),gra(n),bl(n),bu(n),gt(n),jbound(n)
      do i=1,n
              gra(i)=gt(i)
c----------------------------------------------------------------------
c     Computes gra(x)=gt(y)*(-2*x), considering the
c     transformation y = bu - x**2 .
c----------------------------------------------------------------------
      if(jbound(i).eq.1)then
              gra(i)=-2.d0*gt(i)*x(i)
      else
c----------------------------------------------------------------------
c     Computes gra(x)=gt(y)*(2*x), considering the
c     transformation y = bl + x**2
c----------------------------------------------------------------------
              if(jbound(i).eq.2)then
                      gra(i)=2.d0*gt(i)*x(i)
              else
c----------------------------------------------------------------------
c     Computes gra(x)=gt(y)*(bu-bl)*sin(2*x), considering the
c     transformation y = bl + (bu - bl) * (sin x)**2.
c----------------------------------------------------------------------
                      if(jbound(i).eq.3)then
                              bl1=bu(i)-bl(i)
                              gra(i)=gt(i)*bl1*dsin(2.d0*x(i))
                      end if
              end if
      end if

      end do

      return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c     Hessix computes the Hessian of the transformed problem.
c----------------------------------------------------------------------
      subroutine hessix(n,x,bl,bu,gy,hes,jbound)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c    Input :
c
c        n :  number of variables.
c        x :  current iterate.
c       bl :  vector of lower bounds.
c       bu :  vector of upper bounds.
c       gy :  gradient of the original problem.
c      hes :  vector of dimension n1 = n*(n+1)/2 containing the upper half
c             of the Hessian of the original problem stored columnwise.
c   jbound :  see definition in the main routine.
c
c   Output :
c
c      hes :  Hessian at x.
c-----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x(n),hes(1),bl(n),bu(n),gy(n),jbound(n)
c-----------------------------------------------------------------------
c      Compute the Hessian in the new variables.
c-----------------------------------------------------------------------
      do i=1,n
              xi=x(i)
              i1=i*(i+1)/2
              i2=i1
              k1=i*(i-1)/2+1
              k2=i2-1
              if(jbound(i).eq.1)then
                      hes(i1)=hes(i1)*4.d0*xi**2-2.d0*gy(i)
                      do k=i,n-1
                              i2=i2+k
                              hes(i2)=hes(i2)*(-2.d0*xi)
                      end do
                      do k=k1,k2
                              hes(k)=hes(k)*(-2.d0*xi)
                      end do
              else
                      if(jbound(i).eq.2) then
                              hes(i1)=hes(i1)*4.d0*xi**2+2.d0*gy(i)

                              do k=i,n-1
                                      i2=i2+k
                                      hes(i2)= hes(i2)*2.d0*xi
                              end do

                              do k=k1,k2
                                      hes(k)= hes(k)*2.d0*xi
                              end do
                      else
                              if(jbound(i).eq.3)then
                                      bul=bu(i)-bl(i)
                                      hes(i1)=hes(i1)*(2.d0*bul*
     *           dsin(xi)*dcos(xi))**2+
     *                                2.d0*gy(i)*bul*dcos(2.d0*xi)

                                      do k=i,n-1
                                              i2=i2+k
                                              hes(i2)= hes(i2)*bul*
     *                   dsin(2.d0*xi)
                                      end do

                                      do k=k1,k2
                                              hes(k)= hes(k)*bul*
     *                   dsin(2.d0*xi)
                                      end do

                                      end if
                      end if
              end if
      end do
      return
      end
c  ********************************************************************
c-------------------------------------------------------------------------
c     Subroutine for computing the Householder decomposition
c     of the Hessian matrix H= Qt*T*Q at the current iterate.
c----------------------------------------------------------------------
      subroutine factor(n,n1,hes,qt,d,e,itrid)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c         n:  dimension of the problem.
c        n1:  n*(n+1)/2
c       hes:  vector of dimension n1 containing the upper
c             half of the Hessian stored columnwise.
c     itrid:  parameter such that if equal to
c             0 the Hessian is not a tridiagonal matrix.
c             1 the Hessian is a tridiagonal matrix.
c
c    Output:
c
c        Qt:  orthogonal matrix of the decomposition Qt*T*Q.
c         d:  diagonal of the tridiagonal matrix T.
c         e:  subdiagonal of the tridiagonal matrix T.
c----------------------------------------------------------------------
      implicit real*8 (a-h,o-z)
      dimension hes(n1),qt(n,n),d(n),e(n)

      do j=1,n

              do i=1,n
                      qt(i,j)=0.d0
              end do

              qt(j,j)=1.d0
      end do

      if(itrid.eq.1)then
              e(1)=0.d0
              d(1)=hes(1)

              if(n.ge.2)then
                      kd=3
                      do i=2,n
                              e(i)=hes(kd-1)
                              d(i)=hes(kd)
                              kd=kd+i+1
                      end do
              end if

      else
c----------------------------------------------------------------------
c      Call to the subroutine which computes the Householder
c      decomposition
c----------------------------------------------------------------------
      call dholder(hes,n,n1,d,e)
c----------------------------------------------------------------------
c     Find the orthogonal matrix qt ,product of the
c     Householder transformations.
c----------------------------------------------------------------------
      if(n.gt.1)then
              do i=2,n
                      l= i-1
                      ia=(i*l)/2
                      h=hes(ia+i)
                      if(dabs(h).gt.0.d0)then
                              do j=1,n
                                      s=0.0d0
                                      do k=1,l
                                             s=s+hes(ia+k)*qt(k,j)
                                      end do
                                      s=s/h
                                      do k=1,l
                                           qt(k,j)=qt(k,j)-s*hes(ia+k)
                                      end do
                              end do
                      end if
              end do
      end if
      end if
      return
      end
c  ********************************************************************
c-----------------------------------------------------------------------
c  ********************************************************************
c----------------------------------------------------------------------
c     Subroutine dholder finds the tridiagonal matrix T of
c     decomposition Qt*T*Q, where Qt is an orthogonal matrix
c     using Householder's transformations.
c----------------------------------------------------------------------
      subroutine dholder (a,n,n1,d,e)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c    Input :
c
c        a :  is a vector of dimension n1 = n*(n+1)/2
c             containing the upper half of the symmetric matrix
c             stored columnwise.
c
c        n :  dimension of the problem.
c
c       n1 :  dimension of vector a.
c
c   Output :
c
c        d :  diagonal of the tridiagonal matrix.
c
c        e :  subdiagonal of the tridiagonal matrix.
c
c        a :  the vector a restores information
c             for computing Qt from Householder transformations.
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension a(n1),d(n),e(n)
      data zero/0.d0/
      m=n1-1
      nq=n1-n

      do it=1,n
              ib=n+1-it
              l=ib-1
              s=zero
              sum = zero

              if(l.lt.1)then
                      e(ib)=zero
                      go to 20
              end if

              nk=m

              do k=1,l
                      sum=sum+dabs(a(nk))
                      nk=nk-1
              end do

              if(sum.gt.zero) then
                      nk=m

                      do k=1,l
                              a(nk)=a(nk)/sum
                              s=s+a(nk)*a(nk)
                              nk=nk-1
                      end do

                      fr=a(m)
                      gr=-dsign(dsqrt(s),fr)
                      e(ib)=sum*gr
                      s=s-fr*gr
                      a(m)=fr-gr
                      if(l.eq.1) go to 10
                      fr=zero
                      kl1=1

                      do k=1,l
                              gr=zero
                              ik=nq+1
                              kk=kl1
c----------------------------------------------------------------------
c     Form element of a*u.
c----------------------------------------------------------------------
                      do kl=1,k
                              gr=gr+a(kk)*a(ik)
                              kk=kk+1
                              ik=ik+1
                      end do
                              kp1=k+1

                              if(l.ge.kp1)then
                                      kk=kk+k-1
                                      do kl=kp1,l
                                              gr=gr+a(kk)*a(ik)
                                              kk=kk+kl
                                              ik = ik+1
                                      end do
                              end if
c----------------------------------------------------------------------
c     Form element of p.
c----------------------------------------------------------------------
                              e(k)=gr/s
                              fr=fr+e(k)*a(nq+k)
                              kl1=kl1+k
                      end do

                      ss=fr/(s+s)
c---------------------------------------------------------------------
c     Form reduced a.
c----------------------------------------------------------------------
                      kk=1

              do k=1,l
                      fr=a(nq+k)
                      gr=e(k)-ss*fr
                      e(k)=gr

                      do kl=1,k
                              a(kk)=a(kk)-fr*e(kl)-gr*a(nq+kl)
                              kk=kk+1
                      end do

              end do

10            do kl=1,l
                      a(nq+kl)=a(nq+kl)*sum
              end do

              else
                      e(ib)=zero
              end if

20            d(ib)=a(nq+ib)
              a(nq+ib)=s*sum*sum
              nq=nq-ib+1
              m=m-ib
      end do

      return
      end
c *********************************************************************
c----------------------------------------------------------------------
c     Subroutine tri1 solves linear systems with
c     positive definite symmetric tridiagonal matrices.
c----------------------------------------------------------------------
      subroutine tri1(n,d,e,b)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c    Input :
c
c        n :  order of the tridiagonal matrix.
c        d :  diagonal of the tridiagonal matrix.
c        e :  off-diagonal of the tridiagonal matrix.
c        b :  the right hand side vector.
c----------------------------------------------------------------------
c   Output :
c
c        b :  contains the solution.
c
c----------------------------------------------------------------------
      implicit real*8 (a-h,o-z)
      dimension d(n),e(n),b(n)
c----------------------------------------------------------------------
c      check n=1 case.
c----------------------------------------------------------------------
      if(n.eq.1)then
              b(1)=b(1)/d(1)
              go to 70
      end if

      nm1=n-1
      nm1d2=nm1/2

      if(n.gt.2)then
              kbm1= n-1
c----------------------------------------------------------------------
c     zero top half of subdiagonal and bottom half of superdiagonal.
c----------------------------------------------------------------------
              do k=1,nm1d2
                      t1=e(k)/d(k)
                      d(k+1)=d(k+1)-t1*e(k)
                      b(k+1)=b(k+1)- t1*b(k)
                      t2=e(kbm1)/d(kbm1+1)
                      d(kbm1)=d(kbm1)- t2*e(kbm1)
                      b(kbm1)=b(kbm1)- t2*b(kbm1+1)
                      kbm1=kbm1-1
              end do

      end if

      kp1=nm1d2+1
c----------------------------------------------------------------------
c     Clean up for possible 2 x 2 block at center.
c----------------------------------------------------------------------
      if(mod(n,2).eq.0) then
              t1= e(kp1)/d(kp1)
              d(kp1+1)=d(kp1+1)-t1*e(kp1)
              b(kp1+1)=b(kp1+1)-t1*b(kp1)
              kp1=kp1+1
      end if
c----------------------------------------------------------------------
c     Back solve starting at the center, going towards the top
c     and bottom.
c----------------------------------------------------------------------
      b(kp1)=b(kp1)/d(kp1)

      if(n.gt.2) then
              k=kp1-1
              ke= kp1+nm1d2 -1
              do kf=kp1,ke
                      b(k)=(b(k)-e(k)*b(k+1))/d(k)
                      b(kf+1)=(b(kf+1)-e(kf)*b(kf))/d(kf+1)
                      k=k-1
              end do
      end if

      if(mod(n,2).eq.0)b(1)=(b(1)-e(1)*b(2))/d(1)
70    return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c     Computes either Ax or A'x where A is a matrix, A' its transpose,
c     and x a vector.
c----------------------------------------------------------------------
      subroutine matmul(n,a,x,ind,y)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c        n :   dimension of the problem
c        a :   nxn matrix
c        x :   n-dimensional vector
c      ind :   if equal to 1 computes Ax
c              if equal to 2 computes A'x
c
c    Output:
c
c        y :   the product as defined by the input parameter ind
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension a(n,n), x(n),y(n)
      go to (10,20)ind

10    do i=1,n
              yi=0.d0

              do j=1,n
                      yi=yi+ a(i,j)*x(j)
              end do

              y(i)=yi
      end do

      go to 30

20    do j=1,n
              yj=0.d0

              do i=1,n
                      yj=yj+a(i,j)*x(i)
              end do

              y(j)=yj
      end do

30    return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c     This subroutine prints the results
c----------------------------------------------------------------------
      subroutine res(n,x,g,vf,nfu,ngr,nh,nit,ier,ibound)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c    Input :
c
c        n :   dimension of the problem
c        x :   best obtained point
c        g :   gradient at x in unconstrained problems.
c              projected gradient at x in constrained problems.
c       vf :   f(x).
c      nfu :   total number of function evaluations.
c      ngr :   total number of gradiente evaluations.
c       nh :   total number of Hessian evaluations.
c      nit :   number of iterations.
c      ier :   0 convergence has been achieved.
c              1 maximum number of function evaluations exceeded.
c              2 failure to converge.
c              3 wrong input in a constrained problem.
c   ibound :   see definition in the main routine.

c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x(n),g(n)

      if(ier.eq.3)then
              write(6,1)
1             format(10(/),
     *' * * * INPUT ERROR IN A CONSTRAINED PROBLEM - STOP * * *',/)
              return
      end if

      do i=1,n
              write(6,10)i,x(i)
              if(mod(i,20).eq.0)pause
      end do

      dnq=dnrm2(n,g,1)
      pause
      write(6,20)n
      write(6,30) vf
      if(ibound.eq.0)write(6,40)dnq
      if(ibound.ne.0)write(6,50)dnq
      write(6,60) nit
      write(6,70) nfu
      if(ngr.ne.0)write(6,80) ngr
      if(nh.ne.0)write(6,90) nh
      write(6,100) ier
      write(6,110)
10    format('   x(',i3,') =',d16.8)
20    format(20(/),10x,9(' -'),' Final results',9(' -'),
     *///,10x,
     *       '   Number of variables              :',i6)
30    format(10x,'   Final function value             :',d11.4)
40    format(10x,'   Norm of the gradient             :',d11.4)
50    format(10x,'   Norm of the projected gradient   :',d11.4)
60    format(10x,'   Number of iterations             :',i6)
70    format(10x,'   Number of function evaluations   :',i6)
80    format(10x,'   Number of gradient evaluations   :',i6)
90    format(10x,'   Number of Hessian evaluations    :',i6)
100   format(10x,'   ier                              :',i6)
110   format(///,10x,26(' -'),//)
      pause
      return
      end

c  ********************************************************************
c----------------------------------------------------------------------
c     Subroutine autova computes the least eigenvalue of
c     the tridiagonal matrix Tk.
c     In case of failure it returns the lowest Gerschgorin bound.
c----------------------------------------------------------------------
      subroutine autova(d,e2,n)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c    Input :
c
c        d :  diagonal of the tridiagonal matrix.
c       e2 :  vector containing the squares of the subdiagonal elements.
c        n :  dimension of the problem.
c
c   Output :
c
c     d(1) :  estimation of the least eigenvalue.
c
c  Warning :  vectors d and e2 are destroyed.
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension d(n),e2(n)
      data tol/0.10842022d-18/,zero/0.d0/
      dlam = zero
      s = zero
c----------------------------------------------------------------------
c     Look for small sub-diagonal entries
c     Define initial shift from lower Gerschgorin bound
c----------------------------------------------------------------------
      e2(1)=zero

      if(n.ge.2)then
              re2=dsqrt(e2(2))
              ush=d(1)-re2

              if(n.gt.2)then
                      do i=2,n-1
                              p=re2
                              if(p.le.tol*(dabs(d(i))+dabs(d(i-1))))
     *            e2(i)=zero
                              re2=dsqrt(e2(i+1))
                              ush=dmin1(d(i)-p-re2,ush)
                      end do
              end if

              if(re2.le.tol*(dabs(d(n))+dabs(d(n-1))))e2(n)=zero
              ush=dmin1(d(n)-re2,ush)
              autov=ush

              do i=1,n
                      d(i)=d(i)-ush
              end do
c----------------------------------------------------------------------
c     QR transformation
c----------------------------------------------------------------------
              delta=d(n)
10            i=n
              f=dabs(tol*ush)
              dlam=dmax1(dlam,f)
              if(delta.le.dlam)go to 20
c----------------------------------------------------------------------
c     Set small sub-diagonal squares to zero
c     for reducing effects of underflows.
c----------------------------------------------------------------------
              do j=2,n
                      if(e2(j).le.(tol*(d(j)+d(j-1)))**2)e2(j)=zero
              end do

              f=e2(n)/delta
              qp=delta+f
              p=1.d0
              k1=n-1

              do ii=1,k1
                      i=n-ii
                      q=d(i)-s-f
                      r=q/qp
                      p=p*r+1.d0
                      ep=f*r
                      d(i+1)=qp+ep
                      delta=q-ep
                      if(delta.le.dlam) go to 20
                      f=e2(i)/q
                      qp=delta+f
                      e2(i+1)=qp*ep
              end do

              d(1)=qp
              s=qp/p
              ush=ush+s
              delta=d(n)-s
              if(s.gt.zero)go to 10
c----------------------------------------------------------------------
c     Return with an estimation of the least eigenvalue.
c----------------------------------------------------------------------
              e2(1)=1
              d(1)=autov
              go to 30
c----------------------------------------------------------------------
c     Convergence.
c----------------------------------------------------------------------
20            d(1)=ush
      end if

30    return
      end
c********************************************************************
c----------------------------------------------------------------------
c     The subroutine funct computes the value of the objective
c     function on the Levenberg-Marquardt curve at the point x1.
c----------------------------------------------------------------------
      subroutine funct(fcn,n,x0,bl,bu,d,e,qt,w,al,f,x1,y,qs,wa,
     *                  ibound,jbound,nfu)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c       fcn:  external function defining the objective function.
c         n:  dimension of the problem.
c        x0:  starting point on the Levenberg-Marquardt curve
c        bl:  vector of lower bounds.
c        bu:  vector of upper bounds.
c  d, e, qt:  corresponding to the Householder factorization
c         w:  vector Q*(-grad(x0))
c        al:  'Levenberg-Marquardt' parameter.
c        wa:  working vector
c    ibound:  see definition in the main routine.
c    jbound:  see definition in the main routine.
c
c    Output:
c
c       x1 :  point on the curve: x0+s(al)
c        f :  f(x1)
c        y :  coordinates of x1 in the original problem.
c       qs :  vector Q*s(al)
c----------------------------------------------------------------------
      implicit real*8 (a-h,o-z)
      dimension x0(n),d(n),e(n),qt(n,n),w(n),qs(n),wa(1),x1(n),
     *          y(n),bl(n),bu(n),jbound(n)
      external fcn
      nar=1
      nt1=0
      nt2=nt1+n
c----------------------------------------------------------------------
c     Set the parameters for tri1
c----------------------------------------------------------------------
      do i=1,n-1
              wa(nt1+i)=e(i+1)
              wa(nt2+i)=d(i)+al
              qs(i)=w(i)
      end do
      wa(nt1+n)=0.d0
      wa(nt2+n)=d(n)+al
      qs(n)=w(n)
c----------------------------------------------------------------------
c     Solve the system ( T+al*In)Q*s(al) = -Q*grad(x0)
c     Find the coordinates of x1 = x0+s(al).
c----------------------------------------------------------------------
      call tri1(n,wa(nt2+1),wa(nt1+1),qs)
      do i=1,n
              sx=0.d0
              do j=1,n
                      sx=sx+qt(i,j)*qs(j)
              end do
              x1(i)=x0(i)+sx
      end do
c----------------------------------------------------------------------
c     Compute f(x1)
c----------------------------------------------------------------------
      if(ibound.eq.0)then
              call fcn(n,x1,f)
      else
              call transf(n,nar,y,bl,bu,2,x1,jbound,ier)
              call fcn(n,y,f)
      end if
      nfu=nfu+1
      return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c     Function ddot computes the inner product of vectors sx,sy
c     This is a version compatible with BLAS
c----------------------------------------------------------------------
      double precision function ddot (n,x,ix,y,iy)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c        n :  length of vectors x and y.
c        x :  vector of lenght max(n*iabs(ix),1).
c       ix :  displacement between elements of x.
c             x(i) is defined as
c             x(1+(i-1)*ix) if ix.ge.0 or
c             x(1+(i-n)*ix) if ix.lt.0.
c        y :  vector of lenght max(n*iabs(iy),1).
c       iy :  displacement between elements of y.
c             y(i) is defined as
c             y(1+(i-1)*iy) if iy.ge.0 or
c             y(1+(i-n)*iy) if iy.lt.0.
c
c    Output:
c
c      ddot:  inner product of vectors x,y
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x(n),y(n)
      ddot=0.d0
      if(n.le.0)return
      if(ix.eq.iy)if(ix-1)10,20,40
10    ix=1
      iy=1
      if(ix.lt.0)ix=(-n+1)*ix+1
      if(iy.lt.0)iy=(-n+1)*iy+1

      do i=1,n
              ddot = ddot+x(ix)*y(iy)
              ix=ix+ix
              iy = iy+iy
      end do

      return
20    m=n-(n/5)*5
      if(m.eq.0)go to 30

      do i=1,m
              ddot=ddot+x(i)*y(i)
      end do

      if(n.lt.5)return
30    mp1=m+1

      do i=mp1,n,5
              ddot = ddot+x(i)*y(i)+x(i+1)*y(i+1)+x(i+2)*y(i+2)
     *              +x(i+3)*y(i+3)+x(i+4)*y(i+4)
      end do

      return
40    ns = n*ix

      do i=1,ns,ix
              ddot = ddot+x(i)*y(i)
      end do

      return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c     This is a version of the standard BLAS routine for
c     computing the euclidean norm of vector x
c----------------------------------------------------------------------
      double precision function dnrm2(n,x,incx)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c        n :   dimension of the problem
c        x :   n-dimensional vector
c     incx :   displacement between elements of x (normally 1)
c
c    Output:
c
c     dnrm2:  //x// = dsqrt(x(1)**2 + ... + x(n)**2)
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x(N)
      data zero/0.d0/,one/1.d0/
c----------------------------------------------------------------------
c     The following values of bound1 and bound2 are for computers
c     implementing the IEEE floating point standard. For older
c     architectures those values must be replaced by
c     data bound1/8.232d-11/,bound2 /1.304d19/
c----------------------------------------------------------------------
      data bound1/3.861d-41/,bound2 /9.737d76/
      if(n.gt.0)go to 10
      dnrm2 = zero
      go to 130
10    assign 30 to next
      s= zero
      nx=n*incx
      i=1
20    go to next, (30,40,70,80)
30    if(dabs(x(i)).gt.bound1)go to 110
      assign 40 to next
      xmax = zero
40    if(dabs(x(i)).gt.zero) go to 42
      go to 120
42    if(dabs(x(i)).gt.bound1) go to 110
      assign 70 to next
      go to 60
50    i=j
      assign 80 to next
      s=(s/x(i))/x(i)
60    xmax=dabs(x(i))
      go to 90
70    if (dabs(x(i)).gt.bound1) go to 100
80    if (dabs(x(i)).le.xmax) go to 90
      s=one+s*(xmax/x(i))**2
      xmax=dabs(x(i))
      go to 120
90    s=s+(x(i)/xmax)**2
      go to 120
100   s=(s*xmax)*xmax
110   bound3=bound2/float(n)

      do j=1,nx,incx
              if(dabs(x(j)).ge.bound3) go to 50
              s=s+x(j)**2
      end do

      dnrm2=dsqrt(s)
      go to 130
120   continue
      i=i+incx
      if(i.le.nx)go to 20
      dnrm2=xmax*dsqrt(s)
130   continue
      return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c     This subroutine prints the results to the file specified in file name
c----------------------------------------------------------------------
      subroutine prntout (fu,n,x0,fopt,eps,ibound,
     *           jbound,bl,bu,wa,nfu,ngr, nh, nit,ier, ichoice, flname)

C !ms$attributes DLLEXPORT :: prntout

c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c    Input :
c
c     All input arguments are described in curvi_ in more detail, except for
c     ichoice and flname.
c
c      fu     :   external function just as specified in curvi_
c      n      :   dimension of the problem
c      x0     :   initial value into curvi_ if ichoice = 1
c                 or best obtained point    if ichoice = 0
c     fopt    :   best value found by curvi_
c
c     eps     :  requested tolerance
c     ibound  :  0/1 variable determining if bounds are active
c     jbound  :  specific information on individual bounds
c     bl      :  Lower bounds
c     bu      :  Upper bounds
c     wa      :  Work vector returned from and passed into curvi_
c     nfu     :  Number of function values
c     ngr     :  Number of gradient values (set to 0 if ichoice = 0)
c     nh      :  Number of hessian values  (set to 0 if ichoice = 0)
c     nit     :  Number of iterations      (set to 0 if ichoice = 0)
c     ier     :  error criteria
c                0 convergence has been achieved.
c                1 maximum number of function evaluations exceeded.
c                2 failure to converge.
c                3 wrong input in a constrained problem.
c    ichoice  :  ichoice is 0 or 1.  Choose 0 if it is to be invoked before
c                a call to the routine and 1 if after a call.
c
c   flname    :  The output file name
c

c----------------------------------------------------------------------
      implicit none

      double precision x0(*), wa(*), bl(*), bu(*)
      double precision temp, eps, fopt, dnrm2, dnq
      integer   ibound, jbound(*), error, nh, i
      integer nfu, ngr, nit, ier, ichoice, n, lwa
      character flname*(*)
      external fu

      error = 0

      if (ichoice .eq. 0) then
      open(26, file = flname)


      write(26, *) 'The initial input for Curvi follows  '

      write(26, *) ' '
      write(26, *) ' '
      lwa = 9*n+n*(n+1)/2+n*n+max(7*n-n*(n+1)/2,0)
      write(26, *) 'Length of working array wa must be at least ', lwa
      if ( nfu .eq. 0) then
          write(26, *) 'Default bound on number of function values  ',
     *                    n*5000 , '   for curvif'
          write(26, *) '                                            ',
     *                    n*1000 , '   for curvig'
          write(26, *) '                                            ',
     *                    n*1000 , '   for curvih'
      else
          write(26, *) 'Bound on number of function values  ', nfu
      endif

      write(26, *) 'Error tolerance  ', eps
      write(26, *) 'Ibound           ', ibound

c         write input information for debugging purposes
c         and for problem preservations

      If( ibound .eq. 0 ) then
c
c         Initialize variables nh, ngr, nit
c
      nh  = 0
      ngr = 0
      nit = 0

      write(26, *) 'There are no bounds on the variables since '
      write(26, *)   'Ibound = 0'
      write(26, *) ' '
      write(26, *) 'The initial projected values'
      write(26, *) ' '
      do i = 1,n
          write(26,1017) i, x0(i)
      enddo
      call fu(n,x0,temp)
      write(26, 1011)
      write(26, *) 'The initial function value is  '
      write(26, 1011)
      write(26, 1020) temp
      write(26, 1011)
      write(26, 1011)

      else


      write(26, 1011)
      write(26, 1010)
      write(26, 1011)

      do i = 1, n
          wa(i) = x0(i)
          if( jbound(i) .eq. 3) then
              write(26, 1012) i, x0(i), bl(i), bu(i), jbound(i)
              if(bl(i) .gt. bu(i) ) then
                  write(26,*) 'The above constraint is inconsistent'
                  error = 1
                  write(26,1011)
               else
                  if (wa(i) .lt. bl(i))  wa(i) = bl(i)
                  if (wa(i) .gt. bu(i))  wa(i) = bu(i)
              endif
          else if( jbound(i) .eq. 2) then
              write(26, 1013) i, x0(i), bl(i), jbound(i)
              if (wa(i) .lt. bl(i))  wa(i) = bl(i)

          else if (jbound(i) .eq. 1) then
              write(26, 1014) i, x0(i), bu(i), jbound(i)
              if (wa(i) .gt. bu(i))  wa(i) = bu(i)

          else if (jbound(i) .eq. 0) then
              write(26, 1015) i, x0(i), jbound(i)
          else
              write(26, 1016) i, x0(i), jbound(i)
              write(26, *) 'This is an undefined condition '
              error = 1
          endif
      enddo

      if (error .eq. 0) then
          call fu(n,wa,temp)
          write(26, 1011)
          write(26, *)  'The initial function value at the projected ini
     *tial point is'

          write(26, 1011)
          write(26, 1020) temp
          write(26, 1011)
          write(26, 1011)
      else
          write(26, *) 'The conditions specified are inconsistent or und
     *efined'
      endif

      endif
      close(26)
      return

      endif
      open(26, access = 'append', file = flname)
      write(26, 1011)
      write(26, *) '************  Output from CURVI  ************'
      write(26, 1011)

1010  format(10x, ' No. ', 10x, 'Initial Value', 10x,
     * 'Lower Bound', 10x, 'Upper Bound', 10x, 'Jbound')
1011  format(' ')
1012  format(10x, i5, 10x, g16.8, 5x,
     * g16.8, 5x, g16.8, 5x, i4)

1013  format(10x, i5, 10x, g16.8, 5x,
     *    g16.8, 26x, i4)

1014  format(10x, i5, 10x, g16.8, 21x,
     *   5x, g16.8, 5x, i4)

1015  format(10x, i5, 10x, g16.8, 5x,
     * 16x, 5x, 16x, 5x, i4)

1016  format(10x, i5, 10x, g16.8, 5x,
     * 14x, '??', 5x, 14x, '??', 5x, i4)

1017  format(10x, i5, 10x, g16.8, 5x,
     * 16x, 5x, 16x, 5x)

1020  format(10x, g16.8)

      if(ier.eq.3)then
              write(26,1)
1             format(10(/),
     *' * * * INPUT ERROR IN A CONSTRAINED PROBLEM - STOP * * *',/)
              return
      end if

c         write output assuming ier < 3
      write(26, 1000)
      write(26, 1001)
      do i=1,n
              write(26,10)i,x0(i)

      end do

      dnq=dnrm2(n,wa(n*n + n +1),1)

      write(26,20)n
      write(26,30) fopt
      if(ibound.eq.0)write(26,40)dnq
      if(ibound.ne.0)write(26,50)dnq
      write(26,60) nit
      write(26,70) nfu
      if(ngr.ne.0)write(26,80) ngr
      if(nh.ne.0)write(26,90) nh
      write(26,100) ier
      write(26,110)
10    format(10x, i5, 10x, g16.8, 10x, g16.8)
20    format(5(/),10x,9(' -'),' Final Summary',9(' -'),
     *///,10x,
     *       '   Number of variables              :',i6)
30    format(10x,'   Final function value             :',d11.4)
40    format(10x,'   Norm of the gradient             :',d11.4)
50    format(10x,'   Norm of the projected gradient   :',d11.4)
60    format(10x,'   Number of iterations             :',i6)
70    format(10x,'   Number of function evaluations   :',i6)
80    format(10x,'   Number of gradient evaluations   :',i6)
90    format(10x,'   Number of Hessian evaluations    :',i6)
100   format(10x,'   ier                              :',i6)
110   format(///,10x,26(' -'),//)
1000  format(10x, ' No. ', 10x, 'Final Value')
1001  format(10x, '_____', 10x, '___________')



      close(26)
      return
      end
