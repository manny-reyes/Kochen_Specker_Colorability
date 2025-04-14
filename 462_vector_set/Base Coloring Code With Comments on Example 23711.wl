(* ::Package:: *)

(* ::Input:: *)
(*P={}*)
(*(*P simply defines an empty set*)*)


(* ::Input:: *)
(*b[x_,y_,z_]:=Piecewise[{{{{z,0,0},{0,z,0},{0,0,z}},x==y==0},{{{0,y,y},{y,0,y},{y,y,0},{0,y,-y},{y,0,-y},{y,-y,0}},x==0&&y==z},{{{0,y,z},{y,0,z},{y,z,0},{0,z,y},{z,0,y},{z,y,0},{0,-y,z},{-y,0,z},{-y,z,0},{0,z,-y},{z,0,-y},{z,-y,0}},x==0&&y!=z},{{{x,x,x},{-x,x,x},{x,-x,x},{x,x,-x}},x==y==z!=0},{{{z,x,x},{x,z,x},{x,x,z},{-z,x,x},{x,-z,x},{x,x,-z},{-x,x,z},{x,-x,z},{-x,z,x},{x,z,-x},{z,-x,x},{z,x,-x}},x==y&&x!=0&&z!=0},{{{x,y,y},{y,x,y},{y,y,x},{-x,y,y},{y,-x,y},{y,y,-x},{-y,y,x},{y,-y,x},{-y,x,y},{y,x,-y},{x,-y,y},{x,y,-y}},y==z&&y!=0&&x!=0},{{{x,y,z},{-x,y,z},{x,-y,z},{x,y,-z},{y,x,z},{-y,x,z},{y,-x,z},{y,x,-z},{y,z,x},{-y,z,x},{y,-z,x},{y,z,-x},{x,z,y},{-x,z,y},{x,-z,y},{x,z,-y},{z,x,y},{-z,x,y},{z,-x,y},{z,x,-y},{z,y,x},{-z,y,x},{z,-y,x},{z,y,-x}},x!=y&&x!=z&&y!=z&&x!=0&&y!=0&&z!=0}}]*)
(*(*b is a piecewise function which takes the components of a vector and returns a set containing all of the different forms of that vector*)*)


(* ::Input:: *)
(*For[i=0, i<=15, i=i+1,*)
(*For[j=i, j<=15, j=j+1,*)
(*For[k=j, k<=15, k=k+1,*)
(*If[IntegerExponent[(i^2+j^2+k^2),5]==0,*)
(*If[GCD[i,j,k]==1,*)
(*AppendTo[P,b[i,j,k]*)
(*]*)
(*]*)
(*]*)
(*]*)
(*]*)
(*]*)
(*(*This is a loop which checks every integer vector with components smaller than 15 to see if its norm squared is divisible by 5. If it is not, then the loop adds the vector to P, creating a set of vectors with norms squared divisible only by primes other than 5*)*)


(* ::Input:: *)
(*P*)
(*(*This is a restatement of P now that we've added all those different elements*)*)


(* ::Input:: *)
(*V=Partition[Flatten[P],3]*)
(*(*P is a set of sets, where each interior set contains all the forms of a certain vector. However, this makes it difficult for mathematica to run code properly. To fix this problem, we create a new list that has all the elements of P (this is the flatten command), but creates new sets, vectors, every three numbers.*)*)


(* ::Input:: *)
(*W={{1,0,0},{1,0,-1},{1,-1,0}}*)
(*(*This is where we designate what our white vectors will be*)*)


(* ::Input:: *)
(*B={}*)
(*(*This is where we designate our black vectors. I didn't have any so I just made this an empty set but one can add them in as necessary.*)*)


(* ::Input:: *)
(*B'={}*)
(*(*Here we have a new empty list. One can think of this as the set for new black vectors that have just been assigned a coloring.*)*)
(*Q=Complement[V,B]*)
(*(*This is the set of vectors that hasn't been colored black yet, so we don't continue checking vectors weve already colored.*)*)
(*For[i=1,i<=Length[Q],i=i+1,*)
(*For[k=1,k<=Length[W],k=k+1,*)
(*If[Q[[i]] . W[[k]]==0,*)
(*AppendTo[B',Q[[i]]],Unevaluated[Sequence[]]]]]*)
(*(*This loop checks to see if any vectors in Q are orthogonal to a white vector. If so, it adds them to B'.*)*)
(*MM=DeleteDuplicates[B']*)
(*(*This creates a new list containing all of the elements from B' without duplicaes.*)*)
(*B=Union[B,MM]*)
(*(*This adds any new black vectors to B.*)*)
(*For[j=1,j<= Length[MM],j=j+1,*)
(*For[l=j, l<= Length[B],l=l+1,*)
(*If[MM[[j]] . B[[l]]==0,*)
(*AppendTo[W,Cross[MM[[j]],B[[l]]]/GCD[Cross[MM[[j]],B[[l]]][[1]],Cross[MM[[j]],B[[l]]][[2]],Cross[MM[[j]],B[[l]]][[3]]]],Unevaluated[Sequence[]]]]]*)
(*(*This loop checks to see if there are any new black vectors in MM orthogonal to any vectors in B, if so it adds the cross product to the list of white vectors *)*)
(*For[j=1,j<= Length[MM],j=j+1,*)
(*For[l=j, l<= Length[MM],l=l+1,*)
(*If[MM[[j]] . MM[[l]]==0,*)
(*AppendTo[W,Cross[MM[[j]],MM[[l]]]/GCD[Cross[MM[[j]],MM[[l]]][[1]],Cross[MM[[j]],MM[[l]]][[2]],Cross[MM[[j]],MM[[l]]][[3]]]],Unevaluated[Sequence[]]]]]*)
(*(*This loop checks to see if there are any new black vectors in MM orthogonal to any other new black vectors in MM, if so it adds the cross product to the list of white vectors *)*)
(*W=DeleteDuplicates[W]*)
(*(*Again, this gets rid of any repetition in the white vectors.*)*)


(* ::Input:: *)
(*Intersection[B,W]*)
(*(*checking for a contraditction*)*)


(* ::Input:: *)
(*B'={}*)
(*Q=Complement[V,B]*)
(*For[i=1,i<=Length[Q],i=i+1,*)
(*For[k=1,k<=Length[W],k=k+1,*)
(*If[Q[[i]] . W[[k]]==0,*)
(*AppendTo[B',Q[[i]]],Unevaluated[Sequence[]]]]]*)
(*MM=DeleteDuplicates[B']*)
(*B=Union[B,MM]*)
(*For[j=1,j<= Length[MM],j=j+1,*)
(*For[l=j, l<= Length[B],l=l+1,*)
(*If[MM[[j]] . B[[l]]==0,*)
(*AppendTo[W,Cross[MM[[j]],B[[l]]]/GCD[Cross[MM[[j]],B[[l]]][[1]],Cross[MM[[j]],B[[l]]][[2]],Cross[MM[[j]],B[[l]]][[3]]]],Unevaluated[Sequence[]]]]]*)
(*For[j=1,j<= Length[MM],j=j+1,*)
(*For[l=j, l<= Length[MM],l=l+1,*)
(*If[MM[[j]] . MM[[l]]==0,*)
(*AppendTo[W,Cross[MM[[j]],MM[[l]]]/GCD[Cross[MM[[j]],MM[[l]]][[1]],Cross[MM[[j]],MM[[l]]][[2]],Cross[MM[[j]],MM[[l]]][[3]]]],Unevaluated[Sequence[]]]]]*)
(*W=DeleteDuplicates[W]*)
(*(*continuing the process of coloring*)*)


(* ::Input:: *)
(*Intersection[B,W]*)
(*(*checking for a contradiction, and we get one!*)*)


(* ::Input:: *)
(*(*In case we don't get a coloring right off the bat, we continue coloring until we have a step where no new black vectors are added, then we run the code one more time to make sure there are no new white vectors which we haven't checked yet, and then we're done. The code has colored all it can from the black and white vectors given*)*)
