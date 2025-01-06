import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_drop_down.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/form_field_controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'choose_repository_model.dart';
export 'choose_repository_model.dart';

class ChooseRepositoryWidget extends StatefulWidget {
  const ChooseRepositoryWidget({
    super.key,
    this.selectedRepo,
  });

  final String? selectedRepo;

  @override
  State<ChooseRepositoryWidget> createState() => _ChooseRepositoryWidgetState();
}

class _ChooseRepositoryWidgetState extends State<ChooseRepositoryWidget> {
  late ChooseRepositoryModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => ChooseRepositoryModel());

    // On page load action.
    SchedulerBinding.instance.addPostFrameCallback((_) async {
      if (!(_model.apiRepoData.isNotEmpty)) {
        _model.apiResultpi6 = await GetRepositoriesCall.call();

        if ((_model.apiResultpi6?.succeeded ?? true)) {
          _model.apiRepoData =
              (_model.apiResultpi6?.jsonBody ?? '').toList().cast<String>();
          safeSetState(() {});
        }
      }
    });

    WidgetsBinding.instance.addPostFrameCallback((_) => safeSetState(() {}));
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).secondaryBackground,
        appBar: AppBar(
          backgroundColor: FlutterFlowTheme.of(context).secondaryText,
          automaticallyImplyLeading: false,
          leading: FlutterFlowIconButton(
            borderColor: Colors.transparent,
            borderRadius: 30.0,
            borderWidth: 1.0,
            buttonSize: 60.0,
            icon: const Icon(
              Icons.arrow_back_rounded,
              color: Colors.white,
              size: 30.0,
            ),
            onPressed: () async {
              context.pushNamed('HomePage');
            },
          ),
          title: Text(
            'Normal Post',
            style: FlutterFlowTheme.of(context).headlineMedium.override(
                  fontFamily: 'Outfit',
                  color: Colors.white,
                  fontSize: 22.0,
                  letterSpacing: 0.0,
                ),
          ),
          actions: const [],
          centerTitle: false,
          elevation: 2.0,
        ),
        body: SafeArea(
          top: true,
          child: Padding(
            padding: const EdgeInsetsDirectional.fromSTEB(24.0, 16.0, 24.0, 0.0),
            child: Column(
              mainAxisSize: MainAxisSize.max,
              children: [
                Padding(
                  padding: const EdgeInsetsDirectional.fromSTEB(0.0, 150.0, 0.0, 0.0),
                  child: Row(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Flexible(
                        child: Container(
                          width: 220.0,
                          height: 40.0,
                          decoration: BoxDecoration(
                            color: FlutterFlowTheme.of(context).primary,
                            borderRadius: BorderRadius.circular(14.0),
                          ),
                          alignment: const AlignmentDirectional(0.0, 0.0),
                          child: Padding(
                            padding: const EdgeInsetsDirectional.fromSTEB(
                                16.0, 0.0, 16.0, 0.0),
                            child: Text(
                              'Select a repository',
                              style: FlutterFlowTheme.of(context)
                                  .titleSmall
                                  .override(
                                    fontFamily: 'Plus Jakarta Sans',
                                    fontSize: 20.0,
                                    letterSpacing: 0.0,
                                  ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                Padding(
                  padding: const EdgeInsetsDirectional.fromSTEB(0.0, 24.0, 0.0, 12.0),
                  child: FlutterFlowDropDown<String>(
                    controller: _model.selectedRepositoryValueController ??=
                        FormFieldController<String>(
                      _model.selectedRepositoryValue ??= 'NULL',
                    ),
                    options: _model.apiRepoData,
                    onChanged: (val) async {
                      safeSetState(() =>
                          _model.selectedRepositoryValue = val); // RepoAction

                      context.pushNamed(
                        'normalPostDetails',
                        queryParameters: {
                          'selectedRepo': serializeParam(
                            _model.selectedRepositoryValue,
                            ParamType.String,
                          ),
                        }.withoutNulls,
                      );
                    },
                    width: double.infinity,
                    height: 50.0,
                    textStyle: FlutterFlowTheme.of(context).bodyMedium.override(
                          fontFamily: 'Plus Jakarta Sans',
                          color: FlutterFlowTheme.of(context).primaryText,
                          fontSize: 16.0,
                          letterSpacing: 0.0,
                          fontWeight: FontWeight.w500,
                        ),
                    hintText: 'Select...',
                    icon: Icon(
                      Icons.keyboard_arrow_down_rounded,
                      color: FlutterFlowTheme.of(context).secondaryText,
                      size: 24.0,
                    ),
                    fillColor: FlutterFlowTheme.of(context).secondaryBackground,
                    elevation: 0.0,
                    borderColor: FlutterFlowTheme.of(context).secondaryText,
                    borderWidth: 1.0,
                    borderRadius: 8.0,
                    margin: const EdgeInsets.all(14.0),
                    hidesUnderline: true,
                    isOverButton: false,
                    isSearchable: false,
                    isMultiSelect: false,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
